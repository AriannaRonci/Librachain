//SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4.0;

contract OnChainManager {
    mapping(string => address[]) public shardsMapping;
    mapping (string => int) public shardsBalance;
    event AddedToDict(bool result);

    //add element to dictionary
    function addToDictionary(string memory shardAddress, address contractAddress) public{
        shardsMapping[shardAddress].push(contractAddress);
        shardsBalance[shardAddress]++;
        emit AddedToDict(true);
    }

    //get list of contract addresses of a given shard
    function getAddressList(string memory shardAddress) public view returns (address[] memory){
        return shardsMapping[shardAddress];
    }

    //get balance of a given shard
    function getBalance(string memory shardAddress) public view returns (int){
        return shardsBalance[shardAddress];
    }

    function compareStrings(address a, address b) public pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
}
