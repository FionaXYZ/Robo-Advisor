import React from 'react';
import TextField from '@material-ui/core/TextField';
  
export default function ISINOption({isin,setIsin}) {
    console.log(isin)

    return (
      <>
        <TextField label="ISIN" id="standard-basic" defaultValue={isin} onChange={e=>setIsin(e.target.value)}/>
        <TextField id="filled-basic" label="Filled" variant="filled"/>
        <TextField id="outlined-basic" label="Outlined" variant="outlined"/> <br/>
      </>
    );
}