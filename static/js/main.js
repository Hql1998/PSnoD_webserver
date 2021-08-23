function clear_textarea(){
    textarea = document.querySelector("#pred-textarea");
//    textarea = document.getElementById("pred-textarea");
    textarea.value = "";
}

function generate_example(){
    exampel_text = ">NR_002987.1 Homo sapiens small nucleolar RNA, H/ACA box 61 (SNORA61), small nucleolar RNA type"+"\n"+"ATCCTCCTGATCCCTTTCCCATCGGATCTGAACACTGGTCTTGGTGGTCGTAAAAGGAGGAAAAGTAATAGTGAAGCTGGCCTAAATGTTGTAATCTGGTATATGGCATGTGGGCTAGTTTCAGACAGGT";
    textarea = document.querySelector("#pred-textarea");
    textarea.value = exampel_text;
}