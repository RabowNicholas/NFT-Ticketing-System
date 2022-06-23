//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./Event.sol";

contract EventFactory is Ownable {

  Event internal eventContract;
  Event[] public events;

  uint256 public costOfEvent;

  mapping(address=>Event[]) public eventsOwnedBy;


  event EventCreated(address account, address eventAddress, uint32 numberOfTickets, string location, string name, uint256 time);

  constructor(uint256 _costOfEvent) public {
    costOfEvent = _costOfEvent;
  }

  function createEvent(uint32 _numberOfTickets, uint256 _costOfTicket, string memory _location, string memory _name, uint256 _time) public payable returns(address){
    require(msg.value >= costOfEvent);
    uint256 daysFromNow = block.timestamp + (_time * 1 days);
    eventContract = new Event(msg.sender, _numberOfTickets,_costOfTicket, _location, _name, daysFromNow); //create new event contract
    events.push(eventContract); //add event to total events list
    //add event to ownedby mapping
    eventsOwnedBy[msg.sender].push(eventContract);

    emit EventCreated(msg.sender, address(eventContract), _numberOfTickets, _location, _name, daysFromNow);
  }

  //Owner functions

  function setCostOfEvent(uint256 _cost) public onlyOwner {
    costOfEvent = _cost;
  }
  function withdraw() public onlyOwner {
    payable(owner()).transfer(address(this).balance);
  }

  //Viewer Functions
  function addressOwnsEvent(address _owner) public view returns(bool) {
    if (eventsOwnedBy[_owner].length == 0) {
      return false;
    } else {
      return true;
    }
  }
}
