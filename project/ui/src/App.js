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
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import { green } from '@material-ui/core/colors';
import mpld3 from 'mpld3';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';


function makeuidfunc(prefix){
  let i = 0;
  return ()=>{i+=1; return prefix+i}
}

let makeISINId=makeuidfunc("isin");


const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      // width: '25ch',
      
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
    return makeDefaultIsinObj(isin,true)
  }
  
  function makeDefaultIsinObj(isin,deleteable=true) {
    return{"isin":isin,"constraint":"None","constraint_op1":null,"deleteable":deleteable,"uid":makeISINId()}
  }

  const [isins,setIsins]=useState([...default_isin.map(makeDefaultIsinObjNotDeleteable),makeDefaultIsinObj('risk-free',false)])
  const [feedback,Setfeedback]=useState({"max_mini":null,"frontier":null,"allocation":null})
  const [open,setOpen]=React.useState(false);
  const [load,setLoad]=React.useState(false)

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
      newArray.splice(idx, 1);
      setIsins(newArray);
    }})
  }

  const handleSubmit=(event)=>{
    // event.preventDefault();
    Setfeedback({"max_mini":null,"frontier":null,"allocation":null});
    axios.post('http://localhost:8000/',{isins}).then((res)=>{
      // debugger;
      console.log(res.data);
      // let x={}
      // eval('let x='+res.data +'; Setfeedback(x.data);');
      Setfeedback(res.data);
      offLoading();
      mpld3.draw_figure("frontier",res.data.frontier);
      mpld3.draw_figure("allocation",res.data.allocation)
    });
    
  }

  console.log(mpld3)
  return (
    <> <Typography variant="h5" component="h2" align="center" >
       <Button variant="outlined" color="primary" onClick={handleClickOpen} align="center">
       Select Your Assets  &nbsp; &nbsp;  {load===true&&<CCircularProgress/>}
      </Button>
      </Typography>
      {/* {load===true&&<CCircularProgress/>} */}
      <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title" fullWidth="true" maxWidth="md" className={classes.root}>
        <DialogTitle id="form-dialog-title">Select Your Assets</DialogTitle>
        {/* <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}> */}
        <DialogContent>
      {isins.map((isin,i)=>
          (<ISINOption isinObj={isin} setIsinObj={factoryUpdateArray(isins,i)} deleteIsin={isin.deleteable?makeDeleteIsin(isins,i):null} key={isin.uid}/>
      ))}
      <Button onClick={()=>{NewIsin(isins)}} color="primary" variant="contained">Add New ISIN</Button>
       </DialogContent>
        <DialogActions>
        <Button variant="contained" type="submit" onClick={()=>{handleSubmit();handleClose();onLoading()}} className={classes.buttonSubmit}>Submit</Button>
        </DialogActions>
        {/* </form> */}
      </Dialog>
  
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

