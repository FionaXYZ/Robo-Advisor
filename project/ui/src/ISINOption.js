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

    return (
      <>
        <TextField label="ISIN" defaultValue={isinObj.isin} onChange={e=>setIsinObj({...isinObj,isin:e.target.value})} variant="outlined"/>
        <TextField select label="Constraints"  defaultValue={isinObj.constraint} onChange={e=>{setIsinObj({...isinObj,constraint:e.target.value})}} 
          SelectProps={{native: true,}}
          helperText="Choose to add constraint"
          variant="outlined" >
          {constraints.map((option) => (
            <option key={option.value} >
              {option.label}
            </option>
          ))}
        </TextField>
        {isinObj.constraint!=="None" && <TextField label={"weight "+isinObj.constraint} helperText="weight should be between 0 and 1" defaultValue={isinObj.constraint_op1} onChange={e=>setIsinObj({...isinObj,constraint_op1:e.target.value})} variant="outlined" />}
        {isinObj.deleteable!==true && <TextField label={"Return rate %"} helperText="Return rate of the saving account" defaultValue={isinObj.rate} onChange={e=>setIsinObj({...isinObj,rate:e.target.value})} variant="outlined" />}
        {isinObj.deleteable!==false && <Button startIcon={<DeleteIcon />} onClick={()=>{deleteIsin()}} color="default" variant="contained"></Button>}
         <br/><br/>
      </>
    );
}