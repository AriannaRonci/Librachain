// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0.0;

/**
 * @title StorageList
 * @dev Store & retrieve value in a variable
 * @custom:dev-run-script ./scripts/deploy_with_ethers.ts
 */
contract StorageList {

    int [] public data = [int(50), -63, 77, -28, 90];  
    /**
     * @dev Store value in variable
     * @param num value to store
     */

    /**
     * @dev Return value 
     * @return value of 'number'
     */
    function retrieve() public view returns (int[] memory){
        return data;
    }

    function aggiungi(int [] memory numbers) public{
        for (uint i=0; i<numbers.length; i++){
            data.push(numbers[i]);
        }
    }
}

