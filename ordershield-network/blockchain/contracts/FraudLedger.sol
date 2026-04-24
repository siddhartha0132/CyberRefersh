// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract FraudLedger {
    
    struct FraudEvent {
        bytes32 userHash;
        bytes32 deviceHash;
        bytes32 addressHash;
        string eventType;
        uint8 riskScore;
        bytes32 eventHash;
        uint256 timestamp;
    }
    
    mapping(bytes32 => FraudEvent[]) private userEvents;
    mapping(bytes32 => uint256) private userEventCount;
    
    event FraudEventAdded(
        bytes32 indexed userHash,
        string eventType,
        uint8 riskScore,
        bytes32 eventHash,
        uint256 timestamp
    );
    
    function addFraudEvent(
        bytes32 _userHash,
        bytes32 _deviceHash,
        bytes32 _addressHash,
        string memory _eventType,
        uint8 _riskScore,
        bytes32 _eventHash
    ) public {
        require(_riskScore >= 1 && _riskScore <= 3, "Invalid risk score");
        
        FraudEvent memory newEvent = FraudEvent({
            userHash: _userHash,
            deviceHash: _deviceHash,
            addressHash: _addressHash,
            eventType: _eventType,
            riskScore: _riskScore,
            eventHash: _eventHash,
            timestamp: block.timestamp
        });
        
        userEvents[_userHash].push(newEvent);
        userEventCount[_userHash]++;
        
        emit FraudEventAdded(
            _userHash,
            _eventType,
            _riskScore,
            _eventHash,
            block.timestamp
        );
    }
    
    function getUserEvents(bytes32 _userHash) public view returns (FraudEvent[] memory) {
        return userEvents[_userHash];
    }
    
    function getRiskEventCount(bytes32 _userHash) public view returns (uint256) {
        return userEventCount[_userHash];
    }
    
    function getLatestEvent(bytes32 _userHash) public view returns (FraudEvent memory) {
        require(userEventCount[_userHash] > 0, "No events found");
        uint256 lastIndex = userEvents[_userHash].length - 1;
        return userEvents[_userHash][lastIndex];
    }
}
