pragma solidity ^0.4.18;

contract NextBlockToken{
    address private owner;
    uint256 private blockOfContractCreation;
    mapping(address=>uint256) public tokenBalances;
    
    
    function NextBlockToken(uint256 _initialSupply) public{
        owner = msg.sender;
        tokenBalances[owner] = _initialSupply;
        blockOfContractCreation = block.number;
    }
    
    function buyTokens(uint256 amount) public{
        assert(block.number== blockOfContractCreation+1);
        assert(amount<=tokenBalances[owner]);
        tokenBalances[owner]-=amount;
        tokenBalances[msg.sender]+=amount;
    }
}