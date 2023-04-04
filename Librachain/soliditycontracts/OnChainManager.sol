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

    function compareStrings(address a, address b) public pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }

    function findString(address[] memory array,address _string) internal pure returns (bool){
    for (uint i = 0; i < array.length; i++) {
        address stringToFind = array[i];
        bool exists = compareStrings(stringToFind, _string);
        if(exists == true) {
            return true;
        }
    }
        return false;
    }

    function getShard(address smartContractAddress) public view returns (string memory){
        string[3] memory shards = ["http://127.0.0.1:8545", "http://127.0.0.1:8546", "http://127.0.0.1:8547"];
        for(uint i=0; i<2; i++){
            string memory shard = shards[i];
            if (findString(shardsMapping[shard], smartContractAddress)==true)
                return shard;
        }
        return "contract not deployed";
    }
}
