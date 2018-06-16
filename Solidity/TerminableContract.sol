pragma solidity ^0.4.18;

contract MainContract{
    address internal owner;
    modifier isOwner(){
        require(msg.sender==owner);
        _;
    }
    function MainContract() public{
        owner = msg.sender;
    }
    function deposit() public payable{
        
    }
    function getBalance() public view isOwner returns(uint256){
        return this.balance;
    }
}
contract ToBeTerminated is MainContract{
    function terminate() public isOwner{
        selfdestruct(msg.sender);
    }
}