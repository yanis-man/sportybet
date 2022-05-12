function _update_global_odd(new_odd)
{
    oldOdd = Number(document.getElementById("global-odd").innerHTML)
    newOdd = (oldOdd * new_odd).toFixed(2)
    localStorage.setItem("globalOdd", newOdd)
    document.getElementById("global-odd").innerHTML = newOdd
}
function placeBet(elmnt)
{
    betOdd = elmnt.getElementsByClassName("bet-odd")[0].innerHTML
    elmnt.classList.add("clicked")
    betButtonPressedId = elmnt.getAttribute("id")

    //get the whole bet element box
    targetBetBox = document.getElementById(betButtonPressedId.split("-")[0])
    targetButtonList = targetBetBox.getElementsByClassName("bet-button")

    //sets the other buttons as disabled
    for(let i = 0; i < targetButtonList.length; i++)
    {
        targetButtonList[i].removeAttribute('onclick')
        targetButtonList[i].setAttribute('disabled', true)
    }

    document.getElementsByClassName("selected-bet-list")[0].appendChild(targetBetBox)
    _update_global_odd(betOdd)
}

document.getElementById("mise").addEventListener("input", (e) => {
    newMise = Number(document.getElementById("mise").value)
    odd = parseFloat(document.getElementById("global-odd").innerHTML)

    document.getElementById("gains").innerHTML = Math.floor(newMise * odd)
})
function saveBet()
{
    let wantedBets = {"globalOdd":document.getElementById('global-odd').innerHTML, "betAmount":document.getElementById('mise').value, "betsList":[]} // form : id : pred
    selectedBets = document.getElementsByClassName('selected-bet-list')[0].children
    for(let i = 0; i < selectedBets.length; i++)
    {
        singleBet = selectedBets[i]

        singleBetId = String(singleBet.getAttribute('id'))
        singleBetButtons = singleBet.getElementsByClassName('bet-button')
        
        for(let j = 0; j < singleBetButtons.length; j++)
        {
            if (singleBetButtons[j].classList.contains('clicked'))
            {
                // gets the atteched id (1,2,3)
                prediction = singleBetButtons[j].getAttribute('id').split('-')[1]
                wantedBets.betsList.push({[singleBetId]:prediction})
                break;
            }
        }
    }
    console.log(wantedBets)
    $.ajax({
        method:"post",
        url: "api/placeBet",
        contentType: "application/json",
        data: JSON.stringify(wantedBets)
    })
}