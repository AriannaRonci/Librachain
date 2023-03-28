//SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.9.0;

contract OnChainManager {
    mapping(string => address[]) public shardsMapping;
    mapping (string => int) public shardsBalance;

    //add element to dictionary
    function addToDictionary(string memory shardAddress, address contractAddress) public returns (bool){
        shardsMapping[shardAddress].push(contractAddress);
        shardsBalance[shardAddress]++;
        return true;
    }

    //get list of contract addresses of a given shard
    function getAddressList(string memory shardAddress) public view returns (address[] memory){
        return shardsMapping[shardAddress];
    }

    //get balance of a given shard
    function getBalance(string memory shardAddress) public view returns (int){
        return shardsBalance[shardAddress];
    }
}