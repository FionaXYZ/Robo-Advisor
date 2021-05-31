import React,{useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ISINOption from './ISINOption'
import Button from '@material-ui/core/Button';
import axios from 'axios';

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

  const handleSubmit=event=>{
    event.preventDefault();
    axios.post('http://localhost:8000/',{isins}).then((res)=>{console.log(res.data)});
  }

  console.log(isins)
  return (
    <>
    <form className={classes.root} noValidate autoComplete="off" onSubmit={handleSubmit}>
    {isins.map((isin,i)=>
        (<ISINOption isinObj={isin} setIsinObj={factoryUpdateArray(isins,i)} deleteIsin={isin.deleteable?makeDeleteIsin(isins,i):null} key={isin.uid}/> 
    ))}

    <Button onClick={()=>{NewIsin(isins)}} color="primary" variant="contained">Add New ISIN</Button>
    <Button type="submit" variant="outlined" color="primary">Submit</Button>
    </form>
    </>
  )
}


