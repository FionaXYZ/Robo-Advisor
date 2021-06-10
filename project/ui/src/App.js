import React,{useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ISINOption from './ISINOption'
import Button from '@material-ui/core/Button';
import axios from 'axios';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { green } from '@material-ui/core/colors';
import mpld3 from 'mpld3';
import CircularProgress from '@material-ui/core/CircularProgress';
import ImportContactsRoundedIcon from '@material-ui/icons/ImportContactsRounded';
// used some example components from Material-UI website to construct the web page


function makeuidfunc(prefix){
  let i = 0;
  return ()=>{i+=1; return prefix+i}
}

let makeISINId=makeuidfunc("isin");


const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  dialogspace:{
    margin: theme.spacing(1),
    position: 'relative',
  },
  buttonSubmit:{
    color: 'white' ,
    backgroundColor: green[500],
    '&:hover': {
      backgroundColor: green[700],
    },
  },
}));

const useStylesCircle = makeStyles((theme) => ({
  root: {
    position: 'relative',
  },
  bottom: {
    color: theme.palette.grey[theme.palette.type === 'light' ? 200 : 700],
  },
  top: {
    color: '#1a90ff',
    animationDuration: '550ms',
    position: 'absolute',
    left: 0,
  },
  circle: {
    strokeLinecap: 'round',
  },
}));


function CCircularProgress(props) {
  const classes = useStylesCircle();

  return (
    <div className={classes.root}>
      <CircularProgress
        variant="determinate"
        className={classes.bottom}
        size={40}
        thickness={4}
        {...props}
        value={100}
      />
      <CircularProgress
        variant="indeterminate"
        disableShrink
        className={classes.top}
        classes={{
          circle: classes.circle,
        }}
        size={40}
        thickness={4}
        {...props}
      />
    </div>
  );
}


export default function AssetSelection() {
  const classes=useStyles();
  const default_isin=['LU1053186349','IE00B3VNP587','LU0712206050','LU1041109759','IE00B530JS22'];

  function makeDefaultIsinObjNotDeleteable(isin){
    return makeDefaultIsinObj(isin,true,"Empty")
  }
  
  function makeDefaultIsinObj(isin,deleteable=true,rate="Empty") {
    return{"isin":isin,"constraint":"None","constraint_op1":null,"deleteable":deleteable,"rate":rate,"uid":makeISINId()}
  }

  const [isins,setIsins]=useState([...default_isin.map(makeDefaultIsinObjNotDeleteable),makeDefaultIsinObj('risk-free',false,0.45)])
  const [feedback,Setfeedback]=useState({"max_mini":null,"frontier":null,"allocation":null})
  const [open,setOpen]=React.useState(false);
  const [load,setLoad]=React.useState(false)
  const [ifram,setIframe]=React.useState(false)


  const handleIframeOpen=()=>{
    setIframe(true);
  };

  const handleIframeClose=()=>{
    setIframe(false);
  };

  const handleClickOpen=()=>{
    setOpen(true);
  };

  const handleClose=()=>{
    setOpen(false);
  };

  const onLoading=()=>{
    setLoad(true);
  };

  const offLoading=()=>{
    setLoad(false);
  };

  function factoryUpdateArray(array,idx) {
    return (newVal=>{
      let newArray=[...array]
      newArray[idx]=newVal;
      setIsins(newArray);
    })
  }

  function NewIsin(array){
      let newArray=[...array]
      newArray.push(makeDefaultIsinObj(""))
      setIsins(newArray);
  }

  
  function makeDeleteIsin(array,idx){
    return (()=>{
    let newArray=[...array];
    if (idx>-1) {
      newArray.splice(idx,1);
      setIsins(newArray);
    }})
  }

  const handleSubmit=(event)=>{
    Setfeedback({"max_mini":null,"frontier":null,"allocation":null});
    axios.post('http://localhost:8000/',{isins}).then((res)=>{
      Setfeedback(res.data);
      offLoading();
      mpld3.draw_figure("frontier",res.data.frontier);
      mpld3.draw_figure("allocation",res.data.allocation)
    });
    
  }

  return (
    <> 
    {/* educational link on Markowitz model */}
    <Button onClick={handleIframeOpen}>
    <ImportContactsRoundedIcon color="primary" fontSize="large"></ImportContactsRoundedIcon>
    </Button>
     <Dialog open={ifram} onClose={handleIframeClose} aria-labelledby="form-dialog-title" fullScreen="true" className={classes.root}>
    <DialogTitle>
    </DialogTitle>
    <DialogContent>
    <iframe src="https://en.wikipedia.org/wiki/Markowitz_model" width="100%" height="100%"></iframe>
   </DialogContent>
   <DialogActions>
   <Button variant="contained" color="primary" onClick={()=>{handleIframeClose()}}>Close</Button>
   </DialogActions>
  </Dialog>

   {/* User input on setting assets and constraints */}
      <Typography variant="h5" component="h2" align="center" >
       <Button variant="outlined" color="primary" onClick={handleClickOpen} align="center">
       Select Your Assets  &nbsp; &nbsp;  {load===true&&<CCircularProgress/>}
      </Button>
      </Typography>
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title" fullWidth="true" maxWidth="md" className={classes.root}>
        <DialogTitle id="form-dialog-title">Select Your Assets</DialogTitle>
        <DialogContent>
      {isins.map((isin,i)=>
          (<ISINOption isinObj={isin} setIsinObj={factoryUpdateArray(isins,i)} deleteIsin={isin.deleteable?makeDeleteIsin(isins,i):null} key={isin.uid}/>
      ))}
      <Button onClick={()=>{NewIsin(isins)}} color="primary" variant="contained">Add New ISIN</Button>
       </DialogContent>
        <DialogActions>
        <Button variant="contained" type="submit" onClick={()=>{handleSubmit();handleClose();onLoading()}} className={classes.buttonSubmit}>Submit</Button>
        </DialogActions>
      </Dialog>

  {/* Showing result from Markowitz model */}
     {feedback.max_mini!==null&&  <Card className={classes.root}>
      <CardContent>
        <Typography variant="h5" component="h2" align="center" >
         Maximum return available:{feedback.max_mini.range_max}    &nbsp; &nbsp; &nbsp; &nbsp;   &nbsp; &nbsp;     Minimum return available: {feedback.max_mini.range_min}<br/> 
        </Typography>
      </CardContent>
    </Card>}
    {feedback.frontier!==null&&<Card className={classes.root}>
      <CardContent>
        <Typography variant="h5" component="h2" align="center" id="frontier">
        </Typography>
      </CardContent>
    </Card>}
    {feedback.allocation!==null&&  <Card className={classes.root}>
      <CardContent>
        <Typography variant="h5" component="h2" align="center" id="allocation">
        </Typography>
      </CardContent>
    </Card>}

    </>
  )
}

