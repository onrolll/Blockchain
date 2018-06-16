pragma solidity ^0.4.18;

contract TokenShares{
    address private owner;
    uint256 private price;
    uint256 private divident;
    mapping(address=>uint256) private sharesPerAddress;
    mapping(address=>bool) private addressesAllowedToWithdrawFunds;
    address[] private shareHolders;
    
    
    modifier isOwner(){
        require(msg.sender == owner);
        _;
    }
    
    function TokenShares(uint256 _initialSupply, uint256 _pricePerShare,uint256 _divident) public {
        owner = msg.sender;
        price = _pricePerShare * 1 ether;
        divident = _divident * 1 ether;
        sharesPerAddress[owner] = _initialSupply;
        addressesAllowedToWithdrawFunds[owner] = true;
        shareHolders.push(owner);
    }
    function getPricePerShare() view public returns(uint256){
        return price/1 ether;
    }
    function calculateTransactionCost(uint256 amount) view public returns(uint256){
        return (amount * price) / 1 ether;
    }
    function buyShares(uint256 amount) public payable{
        assert(amount<=sharesPerAddress[owner]);
        //overflow precautions
        assert(sharesPerAddress[msg.sender] < sharesPerAddress[msg.sender] + amount);
        assert(msg.value == price * amount);
        
        sharesPerAddress[owner] -= amount;
        sharesPerAddress[msg.sender] += amount;
        shareHolders.push(msg.sender);
    }
    function getShareHolders() view public isOwner returns(address[]){
        return shareHolders;
    }
    function allowWithdrawal(address _address) public isOwner {
        addressesAllowedToWithdrawFunds[_address] = true;
    }
    function depositEarnings() public isOwner payable{
        
    }
    function getBalance() public view isOwner returns(uint256 _balance){
        _balance = this.balance / 1 ether;
        return;
    }
    function getNumberOfShares(address _address) public view returns(uint256 _numberOfShares) {
        require(msg.sender == _address || msg.sender == owner);
        _numberOfShares = sharesPerAddress[_address];
        return;
    }
    function withdaw() public{
        require(sharesPerAddress[msg.sender]>0);
        require(this.balance>= sharesPerAddress[msg.sender] * divident);
        require(addressesAllowedToWithdrawFunds[msg.sender] == true);
        msg.sender.transfer(sharesPerAddress[msg.sender] * divident);
        sharesPerAddress[msg.sender] = 0;
        addressesAllowedToWithdrawFunds[msg.sender] = false;
    }
    
}