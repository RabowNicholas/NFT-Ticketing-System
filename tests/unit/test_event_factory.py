from brownie import (
    EventFactory,
    Event,
    exceptions,
    accounts,
    Contract
)
from scripts.helpful_scripts import (
    get_account
)
import pytest
import time

cost_of_event = 1e18
cost_of_ticket = 1e16

#####################
#EVENT CREATOR TESTS#
#####################

def test_create_event():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})

    #ACT
    create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})

    #ASSERT
    #check event firing
    event = create_event.events["EventCreated"]
    assert event["account"] == account.address
    assert event["numberOfTickets"] == 100000
    assert event["location"] == "Vivint Arena"
    assert event["name"] == "Utah Jazz"
    assert pytest.approx(event["time"],time.time() + (10 * 86400))
    event_address = event['eventAddress']
    print(f"Event Created at : {event_address}")
    #check new event was added to list of events
    assert event_address == event_factory.events(0)
    #check new event was added to event owners list of events
    assert event_address == event_factory.eventsOwnedBy(account, 0)
    #check ownership of event
    event_contract = Event.at(event_address)
    assert account.address == event_contract.owner()

def test_create_event_insufficent_payment():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})

    #ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
            create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz", 10, {"from": account, "value": 0})

###########################
#EVENT FACTORY OWNER TESTS#
###########################

def test_set_cost_of_event():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(0, {"from": account})

    #ACT
    event_factory.setCostOfEvent(cost_of_event, {"from": account});

    #ASSERT
    assert cost_of_event == event_factory.costOfEvent();

def test_set_cost_non_owner():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(0, {"from": account})

    #ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        event_factory.setCostOfEvent(cost_of_event, {"from": accounts[1]});

def test_withdraw_event():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    #ACT
    init_owner_eth_balance = account.balance()
    withdraw = event_factory.withdraw({"from": account})

    #ASSERT
    assert account.balance() == init_owner_eth_balance + cost_of_event

def test_withdraw_non_owner_event():
    #ARRANGE
    account = get_account()
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})
    #ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        event_factory.withdraw({"from": accounts[1]})

#######################
#VIEWER FUNCTION TESTS#
#######################

def test_address_owns_event():
    #ARANGE
    account = get_account()
    non_event_owner = accounts[1]
    event_factory = EventFactory.deploy(cost_of_event, {"from": account})
    create_event = event_factory.createEvent(100000,cost_of_ticket, "Vivint Arena", "Utah Jazz",10, {"from": account, "value": cost_of_event})

    #ACT
    actual_ret_val_event_owner = event_factory.addressOwnsEvent(account)
    actual_ret_val_non_event_owner = event_factory.addressOwnsEvent(non_event_owner)

    #ASSERT
    assert actual_ret_val_event_owner == True
    assert actual_ret_val_non_event_owner == False

def main():
    pass
