//SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.0.0;

contract OnChainManager {
    mapping(uint => mapping(address => bool)) public shardsMapping;
    event AddedToDict(bool result);

    //add element to dictionary
    function addToDictionary(uint shardAddress, address contractAddress) public {
        shardsMapping[shardAddress][contractAddress] = true;
        emit AddedToDict(true);
    }

    //check if smart contract is deployed inside
    function isValidAddress(uint shardAddress, address contractAddress) public view returns (bool){
       if(shardsMapping[shardAddress][contractAddress]==true)
            return true;
        else
            return false;
    }
}
