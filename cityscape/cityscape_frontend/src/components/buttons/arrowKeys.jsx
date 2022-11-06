import React from 'react';
import { Button } from 'antd';
import './button.css'

const ArrowKeys = () => {

    return (
        <>
            <div>
                <Button 
                    className='ArrowkeysUD'
                    shape="round"
                    size='large'
                >
                        ↑ 
                </Button>
                <div>
                    <Button 
                        className='ArrowkeysL'
                        shape="round"
                        size='large'
                    >
                        ←
                    </Button>
                    <Button 
                        className='ArrowkeysR'
                        shape="round"
                        size='large'
                    >   →
                    </Button>
                </div>
                <Button 
                    className='ArrowkeysUD'
                    shape="round"
                    size='large'
                >
                    ↓
                </Button>
            </div>
            <div style={{display:'flex', flexDirection:'column'}}>
                <Button 
                    className='DepthIn'
                    shape="round"
                    size='large'
                >
                    Move In (z+) 
                </Button>
                <Button 
                    className='DepthOut'
                    shape="round"
                    size='large'
                >
                    Move Out (z-) 
                </Button>
            </div>
        </>
    )
}

export default ArrowKeys