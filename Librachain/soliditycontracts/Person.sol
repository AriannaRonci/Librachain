// SPDX-License-Identifier: MIT

pragma solidity >=0.4.0.0;

contract Person {
    string private name;
    uint256 private age;

    function setName(string memory _name) public {
        name = _name;
    }

    function getName() public view returns (string memory) {
        return name;
    }

    function setAge(uint256 _age) public {
        age = _age;
    }

    function getAge() public view returns (uint256) {
        return age;
    }
}