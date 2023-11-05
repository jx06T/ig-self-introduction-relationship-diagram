injection_button = """
var button = document.createElement('button');
button.id = "jx06BT"
button.innerHTML = '開始抓取';
button.onclick = function() {
    alert('開始抓取');
};

button.style.position = 'fixed';
button.style.top = '20px'; 
button.style.right = '20px';
button.style.backgroundColor = 'rgb(205 42 200)'; 
button.style.borderRadius = '7px';
button.style.border = '2px solid #953db6'; 
button.style.cursor = 'pointer'; 
button.style.width = '100px'; 
button.style.height = '35px'; 

document.body.appendChild(button);

var input1 = document.createElement('input');
input1.type = 'text';
input1.id = 'jx06I1';
input1.placeholder = '300 最大次數';
input1.style.position = 'fixed';
input1.style.top = '105px';
input1.style.right = '20px';
input1.style.backgroundColor = 'rgb(255 163 219)';
input1.style.borderRadius = '7px';
input1.style.border = '2px solid #953db6';
input1.style.cursor = 'pointer';
input1.style.padding = '5px';  
input1.style.width = '100px'; 
input1.style.textAlign = 'center'; 
input1.style.width = '100px'; 
input1.style.height = '20px'; 
input1.title = '最多可以讀取多少人資料';
input1.onkeypress = function (e) {
    var key = String.fromCharCode(e.which);
    if (!/^\d+$/.test(key)) {
        e.preventDefault();
    }
};

// 创建第二个输入框
var input2 = document.createElement('input');
input2.type = 'text';
input2.placeholder = '4 掃描層數';
input2.id = 'jx06I2';
input2.style.position = 'fixed';
input2.style.top = '65px';
input2.style.right = '20px';
input2.style.backgroundColor = 'rgb(255 163 219)';
input2.style.borderRadius = '7px';
input2.style.border = '2px solid #953db6';
input2.style.cursor = 'pointer';
input2.style.padding = '5px';  
input2.style.width = '100px';  
input2.style.textAlign = 'center';  
input2.style.width = '100px'; 
input2.style.height = '20px'; 
input2.title = '與開始者的關係層數限制';
input2.onkeypress = function (e) {
    var key = String.fromCharCode(e.which);
    if (!/^\d+$/.test(key)) {
        e.preventDefault();
    }
};

document.body.appendChild(input2);
document.body.appendChild(input1);


    """

remove_button = """
    let button = document.querySelector('#jx06BT')
    button.remove()
    """

remove_button2= """
    let button = document.querySelector('#jx06BT2')
    button.remove()
    """

note = """
var div1 = document.createElement('div');
div1.id = 'jx06D2';
div1.style.position = 'fixed';
div1.style.top = '20px';
div1.style.left = '20px';
div1.style.backgroundColor = 'rgb(255 217 240)';
div1.style.borderRadius = '7px';
div1.style.border = '2px solid rgb(172 41 221)';
div1.style.cursor = 'pointer';
div1.style.padding = '10px';  
div1.style.width = '350px'; 
div1.style.height = '200px'; 
div1.style.fontFamily = 'Arial, sans-serif';
div1.innerText = `1.登入自己帳號後
2.找到要掃描的人主頁
3.按下ctrl+alt+g叫出工具欄
（掃描過程中ctrl+alt+g暫停）

提示：
建議搭配vpn避免ip被封鎖或降速
登入帳號可以減少被限速的機率
不想登入帳號請利用網址列找到要掃描的主頁
`

document.body.appendChild(div1)
"""


injection_button2 = """


var button = document.createElement('button');
button.id = "jx06BT2"
button.innerHTML = '繼續抓取';
button.onclick = function() {
    alert('繼續抓取');
};

button.style.position = 'fixed';
button.style.top = '20px'; 
button.style.right = '20px';
button.style.backgroundColor = 'rgb(205 42 200)'; 
button.style.borderRadius = '7px';
button.style.border = '2px solid #953db6'; 
button.style.cursor = 'pointer'; 
button.style.width = '100px'; 
button.style.height = '35px'; 

document.body.appendChild(button);
"""