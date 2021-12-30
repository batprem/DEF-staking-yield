pragma solidity ^0.8.0;
// SPDX-License-Identifier: MIT
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract DappToken is ERC20{
    constructor() public ERC20("Dapp token", "DAPP"){
        _mint(msg.sender, 1e18);
    }
}

