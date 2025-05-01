function copyAddressDetail(event) {
    event.stopPropagation();
    const text = document.getElementById("address-text").innerText;
    const copiedMsg = document.getElementById("copied-msg");
  
    navigator.clipboard.writeText(text).then(() => {
        copiedMsg.style.display = "inline";
        setTimeout(() => {
            copiedMsg.style.display = "none";
        }, 2000);
    }).catch((err) => {
        console.error("Copy failed", err);
    });
}
  