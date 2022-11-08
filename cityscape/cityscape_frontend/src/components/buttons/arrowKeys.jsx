import React, {useEffect} from 'react';
import { Button } from 'antd';
import './button.css'

const ArrowKeys = () => {

    useEffect(()=>{
        document.addEventListener('keydown', detectKeyPress, true)
    },[])

    const detectKeyPress = (e) =>{
        console.log("key clicked: ", e.key)
        switch(e.key){
            case 'ArrowUp':
                UpFunc();
                break;
            case 'ArrowDown':
                DownFunc();
                break;
            case 'ArrowRight':
                RightFunc();
                break;
            case 'ArrowLeft':
                LeftFunc();
                break;
            case 'd':
                DepthInFunc();
                break;
            case 'f':
                DepthOutFunc();
                break;
            default:
                break;
        }
    }

    const LeftFunc = () =>{
        fetch('/left').then(response => response.json()).then(function(data){
            console.log("DATA IS >> " + data["Status"] )
        })
    }

    const RightFunc = () =>{
        fetch('/right').then(response => response.json()).then(function(data){
            console.log("DATA IS >> " + data["Status"] )
        })
    }

    const UpFunc = () =>{
            fetch('/up').then(response => response.json()).then(function(data){
                console.log("DATA IS >> " + data["Status"] )
            })
    }
    const DownFunc = () =>{
        fetch('/down').then(response => response.json()).then(function(data){
            console.log("DATA IS >> " + data["Status"] )
        })
    }
    const DepthInFunc = () =>{
        fetch('/depthin').then(response => response.json()).then(function(data){
            console.log("DATA IS >> " + data["Status"] )
        })
    }

    const DepthOutFunc = () =>{
        fetch('/depthout').then(response => response.json()).then(function(data){
            console.log("DATA IS >> " + data["Status"] )
        })
    }

    return (
        <>
            <div>
                <Button 
                    className='ArrowkeysUD'
                    shape="round"
                    size='large'
                    // onClick={UpFunc}
                    onKeyDown={UpFunc}
                >
                        ↑ 
                </Button>
                <div>
                    <Button 
                        className='ArrowkeysL'
                        shape="round"
                        size='large'
                        onClick={LeftFunc}
                    >
                        ←
                    </Button>
                    <Button 
                        className='ArrowkeysR'
                        shape="round"
                        size='large'
                        onClick={RightFunc}
                    >   →
                    </Button>
                </div>
                <Button 
                    className='ArrowkeysUD'
                    shape="round"
                    size='large'
                    onClick={DownFunc}
                >
                    ↓
                </Button>
            </div>
            <div style={{display:'flex', flexDirection:'column'}}>
                <Button 
                    className='DepthIn'
                    shape="round"
                    size='large'
                    onClick={DepthInFunc}
                >
                    Move In (z+) 
                </Button>
                <Button 
                    className='DepthOut'
                    shape="round"
                    size='large'
                    onClick={DepthOutFunc}
                >
                    Move Out (z-) 
                </Button>
            </div>
        </>
    )
}

export default ArrowKeys