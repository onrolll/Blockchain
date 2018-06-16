pragma solidity ^0.4.18;
contract RegistryOfCertificates{
    mapping (string=>uint) private certificateHahses;
    address private contractOwner = msg.sender;
    function add(string hash)public {
        require(msg.sender == contractOwner);
        certificateHahses[hash]=1;
    }
    function verify(string hash) view public returns(bool){
        return certificateHahses[hash]!=0;
    }
}
