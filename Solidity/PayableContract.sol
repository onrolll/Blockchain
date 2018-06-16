pragma solidity ^0.4.18;
contract PayableContract{
    address private owner;
    uint256 balance;
    function PayableContract() public{
        owner = msg.sender;
    }
    function deposit() public payable {
        
    }
    function getBalance() public view returns(uint256){
        require(msg.sender==owner);
        return this.balance;
    }
}