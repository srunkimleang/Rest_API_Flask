import './App.css';
import {useState, useEffect} from 'react';
import UserList from './components/UserList';

function App() {

  const [users, setUsers] = useState([])

  useEffect(() => {
    fetch("/user",{
      "method": "GET",
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(resp => resp.json())
    .then(resp => setUsers(resp))
    .catch(error => console.log(error))
  }, []);


  return (
    <div className="App">
      <h1>Flask and ReactJS Course</h1>
        <UserList users= {users}/>
    </div>
  );
}
export default App;
