//SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.9.0;

contract OnChainManager {
    mapping(string => address[]) public shardsMapping;

    //add element to dictionary
    function addToDictionary(string memory shardAddress, address contractAddress) public returns (bool){
        shardsMapping[shardAddress].push(contractAddress);
        return true;
    }

    function getAddressList(string memory shardAddress) public view returns (address[] memory){
        return shardsMapping[shardAddress];
    }

}