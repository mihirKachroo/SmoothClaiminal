const IPFS = require('ipfs')
const OrbitDB = require('orbit-db')

async function createNode() {
        let node = await IPFS.create(
            {
                repo: (() => `repo-${Math.random()}`)(),
                    "Addresses": {
                        "Swarm": [
                            "/ip4/0.0.0.0/tcp/4001"
                        ],
                        "API": "/ip4/127.0.0.1/tcp/5001",
                        "Gateway": "/ip4/127.0.0.1/tcp/8080"
                    }
            }
            );
        try {
            await node.start();
            console.log('Node started!');
        } catch (error) {
            console.error('Node failed to start!', error);
        }
    }
createNode()