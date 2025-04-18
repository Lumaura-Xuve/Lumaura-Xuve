// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title XUVEToken
 * @dev XUVE Token contract with a fixed total supply of 80 million tokens.
 */
contract XUVEToken is ERC20, Ownable {
    // Token distribution addresses
    address public teamWallet;
    address public treasuryWallet;
    address public reserveWallet;
    address public presaleWallet;
    
    // Vesting schedules
    uint256 public teamVestingStart;
    uint256 public teamVestingDuration = 365 days * 3; // 3 years
    uint256 public teamVestingReleased;
    uint256 public teamVestingTotal;
    
    /**
     * @dev Constructor that gives the msg.sender all existing tokens.
     */
    constructor(
        address _teamWallet,
        address _treasuryWallet,
        address _reserveWallet,
        address _presaleWallet
    ) ERC20("XUVE Token", "XUVE") {
        require(_teamWallet != address(0), "Team wallet cannot be zero address");
        require(_treasuryWallet != address(0), "Treasury wallet cannot be zero address");
        require(_reserveWallet != address(0), "Reserve wallet cannot be zero address");
        require(_presaleWallet != address(0), "Presale wallet cannot be zero address");
        
        // Set wallet addresses
        teamWallet = _teamWallet;
        treasuryWallet = _treasuryWallet;
        reserveWallet = _reserveWallet;
        presaleWallet = _presaleWallet;
        
        // Total supply: 80 million tokens
        uint256 totalTokens = 80_000_000 * 10**decimals();
        
        // Token distribution
        uint256 teamAllocation = totalTokens * 20 / 100; // 20%
        uint256 treasuryAllocation = totalTokens * 30 / 100; // 30%
        uint256 reserveAllocation = totalTokens * 10 / 100; // 10%
        uint256 presaleAllocation = totalTokens * 40 / 100; // 40%
        
        // Set vesting details for team
        teamVestingStart = block.timestamp;
        teamVestingTotal = teamAllocation;
        
        // Initial token minting
        _mint(address(this), teamAllocation); // Team allocation held by contract and vested
        _mint(treasuryWallet, treasuryAllocation);
        _mint(reserveWallet, reserveAllocation);
        _mint(presaleWallet, presaleAllocation);
    }
    
    /**
     * @dev Release vested tokens for the team
     */
    function releaseTeamTokens() external {
        require(msg.sender == teamWallet, "Only team wallet can release tokens");
        
        uint256 releasable = getReleasableTeamTokens();
        require(releasable > 0, "No tokens are due for release");
        
        teamVestingReleased += releasable;
        _transfer(address(this), teamWallet, releasable);
        
        emit TeamTokensReleased(releasable);
    }
    
    /**
     * @dev Get the amount of team tokens that are currently releasable
     */
    function getReleasableTeamTokens() public view returns (uint256) {
        return getVestedTeamTokens() - teamVestingReleased;
    }
    
    /**
     * @dev Get the total amount of team tokens that have vested
     */
    function getVestedTeamTokens() public view returns (uint256) {
        if (block.timestamp < teamVestingStart) {
            return 0;
        } else if (block.timestamp >= teamVestingStart + teamVestingDuration) {
            return teamVestingTotal;
        } else {
            return (teamVestingTotal * (block.timestamp - teamVestingStart)) / teamVestingDuration;
        }
    }
    
    /**
     * @dev Update team wallet address (only owner)
     */
    function setTeamWallet(address newTeamWallet) external onlyOwner {
        require(newTeamWallet != address(0), "New team wallet cannot be zero address");
        emit TeamWalletChanged(teamWallet, newTeamWallet);
        teamWallet = newTeamWallet;
    }
    
    /**
     * @dev Update treasury wallet address (only owner)
     */
    function setTreasuryWallet(address newTreasuryWallet) external onlyOwner {
        require(newTreasuryWallet != address(0), "New treasury wallet cannot be zero address");
        emit TreasuryWalletChanged(treasuryWallet, newTreasuryWallet);
        treasuryWallet = newTreasuryWallet;
    }
    
    /**
     * @dev Update reserve wallet address (only owner)
     */
    function setReserveWallet(address newReserveWallet) external onlyOwner {
        require(newReserveWallet != address(0), "New reserve wallet cannot be zero address");
        emit ReserveWalletChanged(reserveWallet, newReserveWallet);
        reserveWallet = newReserveWallet;
    }
    
    /**
     * @dev Update presale wallet address (only owner)
     */
    function setPresaleWallet(address newPresaleWallet) external onlyOwner {
        require(newPresaleWallet != address(0), "New presale wallet cannot be zero address");
        emit PresaleWalletChanged(presaleWallet, newPresaleWallet);
        presaleWallet = newPresaleWallet;
    }
    
    // Events
    event TeamTokensReleased(uint256 amount);
    event TeamWalletChanged(address indexed oldWallet, address indexed newWallet);
    event TreasuryWalletChanged(address indexed oldWallet, address indexed newWallet);
    event ReserveWalletChanged(address indexed oldWallet, address indexed newWallet);
    event PresaleWalletChanged(address indexed oldWallet, address indexed newWallet);
}
