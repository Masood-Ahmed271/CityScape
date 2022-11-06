import {
    DashboardOutlined,
} from '@ant-design/icons';
import './Dashboard.css'
import { Layout, Menu, Button, Divider, Col, Row } from 'antd';
import React, { useState } from 'react';
import ArrowKeys from '../buttons/arrowKeys'

const { Content, Sider } = Layout;
function getItem(label, key, icon, children) {
    return {
        key,
        icon,
        children,
        label,
    };
}

const items = [
    getItem('Dashboard', '1', <DashboardOutlined />),
];

const Dashboard = () => {
    const [collapsed, setCollapsed] = useState(false);

    return (
        <Layout style={{ minHeight: '100vh', }} >
            <Sider className="sideBar" collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
                <Divider />
                <Menu theme="light" defaultSelectedKeys={['1']} mode="inline" items={items} />
                {collapsed ? null :
                    <div className='menuFooter'>
                        <ArrowKeys />
                    </div>}
            </Sider>

            <Layout className="site-layout">
                <Content style={{ margin: '0 16px', }} >
                    <img src={'/video'} alt="live streaming video" width="100%"/>
                </Content>
            </Layout>
        </Layout>
    );
};

export default Dashboard;