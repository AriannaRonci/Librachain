//SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.9.0;

contract OnChainManager {
    mapping (string => int) public shardsBalance;

    //get balance of a given shard
    function getBalance(string memory shardAddress) public view returns (int){
        return shardsBalance[shardAddress];
    }
}