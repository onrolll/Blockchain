pragma solidity ^0.4.18;
contract FallbackExcercise{
    address private owner;
     modifier isOwner(){
        require(msg.sender==owner);
        _;
    }
    function FallbackExcercise() public {
        owner = msg.sender;
    }
    function deposit() public payable{
        
    }
    function getBalance() public view isOwner returns(uint256){
        return this.balance;
    }
    function transfer(address addr,uint256 amount) public isOwner{
        assert(this.balance >= amount);
        addr.transfer(amount);
    }
   
}
contract RecipientContract{
    address private owner;
    modifier isOwner(){
        require(msg.sender==owner);
        _;
    }
    function RecipientContract() public{
        owner = msg.sender;
    }
    function () public payable{
        
    }
    function getBalance() public view isOwner returns(uint256){
        return this.balance;
    }
}