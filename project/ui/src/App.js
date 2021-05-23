import React,{useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ISINOption from './ISINOption'
import Button from '@material-ui/core/Button';


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

  function makeDefualtIsinObj(isin) {
    return{"isin":isin,"constraint":"None","constraint_op1":null}
  }

  const [isins,setIsins]=useState(default_isin.map(makeDefualtIsinObj))

  function factoryUpdateArray(array,idx) {
    return (newVal=>{
      let newArray=[...array]
      newArray[idx]=newVal;
      setIsins(newArray);
    })
  }

  function NewIsin(array){
      let newArray=[...array]
      newArray.push(makeDefualtIsinObj(""))
      setIsins(newArray);
  }

  function DeleteIsin(array,idx){
    let newArray=[...array]
    if (idx>-1) {
      newArray.splice(idx, 1);
      setIsins(newArray);
    }
  }


  console.log(isins)
  
  return (
    <>
    <form className={classes.root} noValidate autoComplete="off">
    {isins.map((isin,i)=>
        (<ISINOption isinObj={isin} setIsinObj={factoryUpdateArray(isins,i)} deleteIsin={()=>{DeleteIsin(isins,i)}} key={i}/> 
    ))}

    <Button onClick={()=>{NewIsin(isins)}} color="primary" variant="contained">Add New ISIN</Button>
    </form>
    </>
  )
}


