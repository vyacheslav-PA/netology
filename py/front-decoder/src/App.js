import './App.css';
// async function getdecodeToken(){
//   let dat = { token: document.getElementById('postToken').value };  
//   try {
//     let response = await fetch('http://0.0.0.0:8000/post_token', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json;charset=utf-8'
//       },
//       body: JSON.stringify(dat)
//     });
//     if (!response.ok) {
//       throw new Error(`Response status: ${response.status}`);
//     }
//   let result = await response.json();
//   result = JSON.stringify(result);
//   result=result.replace(/\\n/g,'\r\n').replace(/\\/g,'');
//   document.getElementById('DecodeToken').value = result ;
//   } catch (error) {
//     console.error(error.message);
//     alert(error.message)
// }
// }
function App() {
  const handleClick = () => {  
    // getdecodeToken();
    try {
    let token=document.getElementById('postToken').value
     var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
  //  alert(JSON.stringify(jsonPayload));
  // let result = JSON.stringify(jsonPayload);
  // result=result.replace(/\\/g,'\r\n');
  // document.getElementById('DecodeToken').value = result ;
  let result = JSON.stringify(jsonPayload);
  result=result.replace(/,/g,',\r\n').replace(/\\/g,'');

  document.getElementById('DecodeToken').value = result ;
    } catch (error) {
      document.getElementById('DecodeToken').value = '' ;
    console.error(error.message);
    alert(error.message)
}
};  
  return (
    <div className="App">
      <header className="App-header">
        <div class="mainarea">
          <div class="token" id="token">
            <div class="a"><label>Токен</label></div>
            <div class="b"><textarea   name="postToken" id="postToken" rows={40} cols={70} /></div>
            <div class ="btn" onClick={handleClick}><button class="btn_decode" id="btn_decode">Расшифровать </button></div>
          </div>  
          <div class="decodeToken" id="decodeToken">
            <div class="a"><label>Расшифровка</label></div>
            <div class="b"><textarea name="DecodeToken" id="DecodeToken" rows={40} cols={70} /></div>
          </div>     
        </div>
      </header>
    </div>
  );
}
export default App;