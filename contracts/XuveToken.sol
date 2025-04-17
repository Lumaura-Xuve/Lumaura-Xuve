// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @custom:security-contact security@lumaura-xuve.io
contract XuveToken is ERC20, ERC20Burnable, Pausable, Ownable {
    uint256 private constant _TOTAL_SUPPLY = 80000000 * 10**18; // 80 million tokens
    
    // Token distribution
    uint256 public teamAllocation = 16000000 * 10**18; // 20%
    uint256 public reserveAllocation = 12000000 * 10**18; // 15%
    uint256 public ecosystemAllocation = 24000000 * 10**18; // 30%
    uint256 public presaleAllocation = 16000000 * 10**18; // 20%
    uint256 public stakingAllocation = 12000000 * 10**18; // 15%
    
    // Vesting periods
    mapping(address => uint256) public vestingPeriodEnd;
    mapping(address => uint256) public allocatedTokens;
    mapping(address => uint256) public releasedTokens;
    
    // Events
    event TokensReleased(address beneficiary, uint256 amount);
    event VestingScheduleCreated(address beneficiary, uint256 amount, uint256 releaseTime);
    
    constructor() ERC20("XUVE Token", "XUVE") {
        // Initial minting to owner - owner will distribute tokens accordingly
        _mint(msg.sender, _TOTAL_SUPPLY);
    }
    
    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }
    
    function createVestingSchedule(
        address beneficiary,
        uint256 amount,
        uint256 vestingDurationDays
    ) external onlyOwner {
        require(beneficiary != address(0), "Beneficiary can't be zero address");
        require(amount > 0, "Amount must be greater than 0");
        require(vestingDurationDays > 0, "Vesting period must be greater than 0");
        
        uint256 releaseTime = block.timestamp + vestingDurationDays * 1 days;
        
        // Transfer tokens to this contract for vesting
        transfer(address(this), amount);
        
        // Set vesting schedule
        vestingPeriodEnd[beneficiary] = releaseTime;
        allocatedTokens[beneficiary] += amount;
        
        emit VestingScheduleCreated(beneficiary, amount, releaseTime);
    }
    
    function releaseVestedTokens(address beneficiary) external {
        require(block.timestamp >= vestingPeriodEnd[beneficiary], "Vesting period not ended yet");
        
        uint256 unreleased = allocatedTokens[beneficiary] - releasedTokens[beneficiary];
        require(unreleased > 0, "No tokens available for release");
        
        releasedTokens[beneficiary] += unreleased;
        _transfer(address(this), beneficiary, unreleased);
        
        emit TokensReleased(beneficiary, unreleased);
    }
    
    function _beforeTokenTransfer(address from, address to, uint256 amount)
        internal
        whenNotPaused
        override
    {
        super._beforeTokenTransfer(from, to, amount);
    }
}
