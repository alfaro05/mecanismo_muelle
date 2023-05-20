"use strict";

function factorial(input_num){
    try{
        let input_int = Number(input_num);
        let result = 1;
        while(input_int>0){
            result = input_int*result;
            input_int -= 1;
        }
        console.log("The result for the input "+input_num+" is:");
        console.log(result);
    }
    catch(err){
        console.log("Invalid input. Please try again");
    }
}
factorial(5);