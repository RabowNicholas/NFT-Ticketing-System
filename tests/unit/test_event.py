from brownie import (
    EventFactory,
    Event,
    exceptions,
    accounts
)
from scripts.helpful_scripts import (
    get_account
)
import pytest

cost_of_event = 1e18
cost_of_ticket = 1e16

##############################
#END USER FUNCTIONALITY TESTS#
##############################

def test_buy_ticket():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(5,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    #ACT
    buy_ticket = event_contract.buyTicket({"from": account, "value": cost_of_ticket})
    #ASSERT
    assert event_contract.isTicketHolder(account.address, {"from": account})
    assert event_contract.ownerOf(0) == account.address
    assert event_contract.balanceOf(account.address) == 1

def test_buy_ticket_sold_out():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(5,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    for i in range(5):
        buy_ticket = event_contract.buyTicket({"from": account, "value": cost_of_ticket})
    #ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        event_contract.buyTicket({"from": account, "value": cost_of_ticket})

def test_buy_ticket_insufficient_payment():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(5,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    #ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        event_contract.buyTicket({"from": account, "value": 0})


#######################
#VIEWER FUNCTION TESTS#
#######################

def test_is_sold_out():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(5,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    for i in range(5):
        buy_ticket = event_contract.buyTicket({"from": account, "value": cost_of_ticket})

    #ACT
    is_sold_out = event_contract.isSoldOut({"from": account})

    #ASSERT
    assert is_sold_out == True

def test_tickets_remaining() :
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(5,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])

    #ACT
    init_tickets_remaining = event_contract.ticketsRemaining()
    buy_ticket = event_contract.buyTicket({"from": account, "value": cost_of_ticket})
    curr_tickets_remaining = event_contract.ticketsRemaining()

    #ASSERT
    assert init_tickets_remaining == 5
    assert curr_tickets_remaining == 4



#####################
#EVENT CREATOR TESTS#
#####################

def test_set_cost_of_ticket():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(5,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    #ACT
    event_contract.setCostOfTicket(1e17,{"from": account})
    #ASSERT
    assert event_contract.costOfTicket() == 1e17

def test_withdraw():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    event_contract.buyTicket({"from":accounts[1], "value": cost_of_ticket})
    #ACT
    init_owner_eth_balance = account.balance()
    withdraw = event_contract.withdraw({"from": account})

    #ASSERT
    assert account.balance() == init_owner_eth_balance + cost_of_ticket

def test_withdraw_non_owner():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    event_contract = Event.at(create_event.events["EventCreated"]["eventAddress"])
    event_contract.buyTicket({"from":accounts[1], "value": cost_of_ticket})


    #ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        event_contract.withdraw({"from": accounts[1]})

def main():
    pass
