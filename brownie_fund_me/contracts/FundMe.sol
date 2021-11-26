// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {

    mapping(address => uint256) public addressToAmountFunded;

    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) {
        // make the owner is the one who deployed this contract
        owner = msg.sender;
        //
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        uint256 minUsd = 50 * 10 ** 18; // everything * 10 ** 18
        require(getConversionRate(msg.value) >= minUsd, "You need to spend more eth!!!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);

        // get ETH -> USD conversion rate

    }

    function getVersion() public view returns (uint256){
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

    // get ETH to USD * 10 ** 18
    function getPrice() public view returns (uint256){
        // AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,int256 answer,,,) = priceFeed.latestRoundData(); 
        return uint256(answer * 10 ** 10); // return ethPriceInUSD * 10 ** 18
    }

    // convert WEI to USD * 10 ** 18
    function getConversionRate(uint256 ethAmountInWei) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        //uint256 ethAmountInUsd = (ethPrice * ethAmountInWei) / 1000000000000000000;
        //uint256 ethAmountInUsd = (ethPrice * ethAmount) / 10 ** 18;
        uint256 ethAmountInUsd = (ethPrice / (10 ** 18)) * ethAmountInWei;

        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Only contract owner can do this");
        _;
    }

    function withDraw() payable onlyOwner public {

        //balance = all money in this contract
        payable(msg.sender).transfer(address(this).balance);
        for (uint256 funderIndex; funderIndex < funders.length; funderIndex ++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }


}