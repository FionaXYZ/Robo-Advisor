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
  const [scope,Setscope]=useState({"range_max":null,"range_min":null})
  const [open, setOpen] = React.useState(false);

  const handleClickOpen=()=>{
    setOpen(true);
  };

  const handleClose=()=>{
    setOpen(false);
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
    axios.post('http://localhost:8000/',{isins}).then((res)=>{console.log(res.data);Setscope(res.data)});
  }

  // console.log(isins)
  return (
    <>
       <Button variant="outlined" color="primary" onClick={handleClickOpen} align="center">
       Select Your Assets
      </Button>
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
        <Button variant="contained" type="submit" onClick={()=>{handleSubmit();handleClose()}} className={classes.buttonSubmit}>Submit</Button>
        </DialogActions>
        {/* </form> */}
      </Dialog>
  
     {scope.range_max!==null&&scope.range_min!==null&&  <Card className={classes.root}>
      <CardContent>
        <Typography variant="h5" component="h2" align="center" >
         Maximum return available:{scope.range_max}    &nbsp; &nbsp; &nbsp; &nbsp;   &nbsp; &nbsp;     Minimum return available: {scope.range_min}
        </Typography>
      </CardContent>
    </Card>}
    </>
  )
}

