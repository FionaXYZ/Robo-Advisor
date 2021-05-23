import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';

const constraints=[
  {
    value:"None",
    label:'None',
  },
  {
    value:'>=',
    label: '≥',
  },
  {
    value:'<=',
    label:'≤',
  },
];


export default function ISINOption({isinObj,setIsinObj,deleteIsin}) {
    console.log(isinObj)

    return (
      <>
        <TextField label="ISIN" id="standard-basic" defaultValue={isinObj.isin} onChange={e=>setIsinObj({...isinObj,isin:e.target.value})} variant="outlined"/>
        <TextField id="select-constraints" select label="Constraints"  defaultValue={isinObj.constraint} onChange={e=>{setIsinObj({...isinObj,constraint:e.target.value})}} 
          SelectProps={{native: true,}}
          helperText="Choose to add constraint"
          variant="outlined" >
          {constraints.map((option) => (
            <option key={option.value} >
              {option.label}
            </option>
          ))}
        </TextField>
        {isinObj.constraint!=="None" && <TextField id="constraints-value" label="0<value<1" defaultValue={isinObj.constraint_op1} onChange={e=>setIsinObj({...isinObj,constraint_op1:e.target.value})} variant="outlined" />}
         <Button startIcon={<DeleteIcon />} onClick={()=>{deleteIsin()}} color="Gray" variant="contained"></Button>
         <br/>
      </>
    );
}