//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract Event is Ownable, ERC721, ERC721Enumerable {
  using Counters for Counters.Counter;
  Counters.Counter private _tokenIdCounter;

  uint32 public numberOfTickets;
  uint256 public costOfTicket;
  uint256 public time;
  string public location;
  string public eventName;
  bool public soldOut;


  address[] internal ticketHolders;

  mapping(address=>bool) internal holdsTicket;

  constructor(address eventOwner, uint32 _numberOfTickets, uint256 _costOfTicket, string memory _location, string memory _name, uint256 _time) ERC721("Ticket", "TCKT") public {
    transferOwnership(eventOwner);
    numberOfTickets = _numberOfTickets;
    costOfTicket = _costOfTicket;
    location = _location;
    eventName = _name;
    time = _time;
    soldOut = false;
  }

  //Public Functions
  function buyTicket() public payable returns(uint256) {
    require(ticketHolders.length < numberOfTickets && msg.value >= costOfTicket);
    ticketHolders.push(msg.sender);
    holdsTicket[msg.sender] = true;
    uint256 newTicketId = _tokenIdCounter.current();
    _mint(msg.sender, newTicketId);
    _tokenIdCounter.increment();

    if (ticketHolders.length == numberOfTickets) {
      soldOut = true;
    }
    return newTicketId;
  }

  //View Functions
  function isSoldOut() public view returns(bool){
    return soldOut;
  }

  function ticketsRemaining() public view returns(uint256) {
    return numberOfTickets - ticketHolders.length;
  }

  //Only Event Creator Functions
  function isTicketHolder(address _holder) public view onlyOwner returns(bool) {
    return holdsTicket[_holder];
  }
  function setCostOfTicket(uint256 _cost) public onlyOwner {
    costOfTicket = _cost;
  }
  function withdraw() public onlyOwner {
    payable(owner()).transfer(address(this).balance);
  }
  function safeMint(address to) public onlyOwner {
    uint256 tokenId = _tokenIdCounter.current();
    _tokenIdCounter.increment();
    _safeMint(to, tokenId);
  }

  // The following functions are overrides required by Solidity.

  function _beforeTokenTransfer(address from, address to, uint256 tokenId)
    internal
    override(ERC721, ERC721Enumerable)
  {
    super._beforeTokenTransfer(from, to, tokenId);
  }

  function supportsInterface(bytes4 interfaceId)
    public
    view
    override(ERC721, ERC721Enumerable)
    returns (bool)
  {
    return super.supportsInterface(interfaceId);
  }
}
