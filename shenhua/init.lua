//定义变量 extension ，包名
local extension = Package("fk_study")
//定义fk_study的中文翻译Fk:
loadTranslationTable
{ 
    ["fk_study"] = "fk学习包",
}
//定义变量 study_sunce ，武将(所在扩展,武将名,势力吴,体力4)
local study_sunce = General(extension, "study_sunce", "wu", 4)
//定义study_sunce的中文翻译Fk:
loadTranslationTable
{ 
    ["study_sunce"] = "孙伯符",
}
//输出扩展
return { extension }