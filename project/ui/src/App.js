import React,{useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ISINOption from './ISINOption'

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export default function AssetSelection() {
  const classes=useStyles();
  const default_isin=['LU1053186349','IE00B3VNP587','LU0712206050','LU1041109759','IE00B530JS22'];
  const [isins,setIsins]=useState(default_isin)

  function factoryUpdateArray(array,idx) {
    return (newVal=>{
      let newArray=[...array]
      newArray[idx]=newVal;
      setIsins(newArray);
    })
  }

  console.log(isins)
  
  return (
    <form className={classes.root} noValidate autoComplete="off">
    {isins.map((isin,i)=>
        (<ISINOption isin={isin} setIsin={factoryUpdateArray(isins,i)}/>)
      )}
    </form>
  )
}



