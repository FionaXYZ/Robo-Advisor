import logo from './logo.svg';
import './App.css';
import React,{useState,useEffect,useMemo,useRef, useReducer,useCallback} from 'react';
// import FunctionContextComponent from './FunctionContextComponent'
// import ClassContextComponent from './ClassContextComponent'
// import {ThemeProvider} from './ThemeContext'
// import Todo from './Todo.js'
// import List from './List.js'
import useLocalStorage from './useLocalStorage.js'
import useUpdateLogger from './useUpdateLogger'


// const ACTIONS={
//   INCREMENT:'increment',
//   DECREMENT:'decrement'
// }

// function reducer(state,action){
//   switch (action.type){
//     case ACTIONS.INCREMENT:
//       return {count: state.count+1}
//     case ACTIONS.DECREMENT:
//       return {count: state.count-1}
//     default:
//       return state
//   }
// }


// export const ACTIONS={
//   ADD_TODO:'add_todo',
//   TOGGLE_TODO:'toggle_todo',
//   DELETE_TODO:'delete_todo'
// }
// function reducer(todos,action) {
//   switch (action.type){
//     case ACTIONS.ADD_TODO:
//       return [...todos,newTodo(action.payload.name)]
//     case ACTIONS.TOGGLE_TODO:
//       return todos.map(todo=>{
//         if (todo.id===action.payload.id){
//           return {...todo,complete: !todo.complete}
//         }
//         return todo
//       })
//     case ACTIONS.DELETE_TODO:
//       return todos.filter(todo=>todo.id!==action.payload.id)
//     default:
//       return todos
//   }
// }
// function newTodo(name) {
//   return {id:Date.now(), name:name, complete:false}
  
// }

function App() {
  // const [state,setState]=useState({count:4,theme:"bule"})
  // const count=state.count
  // const theme=state.theme
  // function decrementCount(){
  //   setState(preState=>{
  //     return {...preState, count:preState.count-1, theme: preState.theme}
  //   })
  // }
  // function incrementCount(){
  //   setState(preState=>{
  //     return {...preState,count:preState.count+1}
  //   })
  // }
  // return (
  //   <>
  //   <button onClick={decrementCount}>-</button>
  //   <span>{count}</span>
  //   <span>{theme}</span>
  //   <button onClick={incrementCount}>+</button>
  //   </> 
  // );

  // const [resourceType,setResourceType]=useState("posts")
  // const [items,Setitems]=useState([])
  // console.log("render")
  // useEffect(()=>{fetch(`https://jsonplaceholder.typicode.com/${resourceType}`)
  // .then(response => response.json())
  // .then(json => Setitems(json))},[resourceType])
  // return(
  //   <>
  //   <div>
  //     <button onClick={()=> setResourceType("posts")}>Posts</button>
  //     <button onClick={()=> setResourceType("users")}>Users</button>
  //     <button onClick={()=> setResourceType("comments")}>Comments</button>
  //   </div>
  //   <h1>{resourceType}</h1>
  //   {items.map(items=>{
  //     return <pre>{JSON.stringify(items)}</pre>
  //   })}
  //   </>
  // )


  // const [windowWidth,setwindowWidth]=useState(window.innerWidth)
  // const handleResize=()=>{
  //   setwindowWidth(window.innerWidth)
  // }
  // useEffect(()=>{
  //   window.addEventListener("resize",handleResize)
  //   console.log("constructor")

  //   return ()=>{
  //     window.removeEventListener("resize",handleResize)
  //     console.log("desstructor")
  //   }
  // },[])
  // return (
  //   <div>{windowWidth}</div>
  // )

  // const [number,setNumber]=useState(0)
  // const [dark, setDark]=useState(false)
  // const doubleNumber=useMemo(()=>{return slowFunction(number)},[number])
  // const themeStyles={backgroundColor:dark?'black':'white',color:dark?'white':'black'}
  // return(
  //   <>
  //   <input type="number" value={number} onChange={e=> {console.log(e) ; setNumber(parseInt(e.target.value))}}/>
  //   <button onClick={()=>setDark(!dark)}>Change Theme</button>
  //   <div style={themeStyles}>{doubleNumber}</div>
  //   </>
  // )
  // function slowFunction(num){
  //   console.log("Calling Slow Function")
  //   for (let i=0; i<=1000000000;i++){}
  //   return num*2
  // }


  // const [name,setName]=useState('')
  // // const renderCount=useRef(0)
  // // useEffect(()=>{renderCount.current=renderCount.current+1})
  // // const inputRef=useRef()
  // // function focus(){
  // //   inputRef.current.focus()
  // // }
  // const prevName=useRef('')
  // useEffect(()=>{prevName.current=name},[name])
  // return(
  //   <>
  //   {/* <input ref={inputRef} value={name} onChange={e=>setName(e.target.value)} /> */}
  //   <input value={name} onChange={e=>setName(e.target.value)} />
  //   <div>My name is {name} and my previous name is {prevName.current}</div>
  //   {/* <div>I rendered {renderCount.current} times</div> */}
  //   {/* <button onClick={focus}>Focus</button> */}

  //   </>
  // )

  // return (
  //   <>
  //   <ThemeProvider>
  //     <FunctionContextComponent/>
  //   </ThemeProvider>
  //   </>
  // )


  // const  [state, dispatch]=useReducer(reducer,{count:0})
  // function incrememt() {
  //   dispatch({type:ACTIONS.INCREMENT})
  // }
  // function decrememt() {
  //   dispatch({type:ACTIONS.DECREMENT})
  // }
  // return(
  //   <>
  //   <button onClick={decrememt}>-</button>
  //   <span>{state.count}</span>
  //   <button onClick={incrememt}>+</button>
  //   </>
  // )


  // const [todos,dispatch]=useReducer(reducer,[])
  // const [name,setName]=useState('')
  // function handleSubmit(e) {
  //   e.preventDefault()
  //   dispatch({type:ACTIONS.ADD_TODO,payload:{name:name}})
  //   setName('')
  // }
  // console.log(todos)
  // return (
  //   <>
  //   <form onSubmit={handleSubmit}>
  //     <input type="text" value={name} onChange={e=>setName(e.target.value)}/>
  //   </form>
  //   {todos.map(todo=>{
  //     return <Todo key={todo.id} todo={todo} dispatch={dispatch}/>
  //   })}
  //   </>
  // )


  // const [number,setNumber]=useState(1)
  // const [dark,setDark]=useState(false)
  // const getItems=useCallback((incrementer)=>{
  //   return [number+incrementer,number+1+incrementer,number+2+incrementer]
  // },[number])
  // const theme={
  //   backgroundColor:dark?'#333':'#FFF',
  //   color:dark?'#FFF':'#333'
  // }
  // return(
  //   <>
  //   <div style={theme}>
  //     <input type='number' value={number} onChange={e=>setNumber(parseInt(e.target.value))}/>
  //     <button onClick={()=>setDark(preDark=>!preDark)}>
  //       Toggle theme
  //     </button>
  //     <List getItems={getItems}/>
  //   </div>
  //   </>
  // )


  const [name,setName]=useLocalStorage('name','')
  useUpdateLogger(name)
  return(
    <>
    <input type='text' value={name} onChange={e=>setName(e.target.value)} />
    </>
  )


}

export default App;
