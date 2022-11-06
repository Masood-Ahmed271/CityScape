import './App.css';
import 'antd/dist/antd.css';
import Dashboard from './components/Dashboard/DashBoard.jsx'

function App() {
  return (
    <>
    <div className="App" style={{ position: 'relative', overflow: "hidden" }}>
      <Dashboard />
    </div>
    </>
  );
}

export default App;
