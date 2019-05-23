# -*- coding: utf-8 -*-

import pytest
from app.utils.text import special_chars, process_text_cn, split_text_by_length


@pytest.mark.usefixtures("app")
def test_text():
    texts = [
        """从男人的角度谈女人的外在美,这个题目真没什么可说的.这是一个简单的、绝对的命题。从远了说，海伦之美引起了特洛伊战争；从近了说，玛丽莲·梦露之美曾经风靡美国。一个男人，只要他视力没有大毛病，就都能欣赏女人的美。
        因为大家都有这种能力，所以这件事常被人用来打比方—孟夫子就喜欢用“目之于色也有同美焉”这个例子来说明大家可以有一致的意见，很显然，他觉得这样一说大家就会明白。谁都喜欢看见好看一点的女人，这一点在男人中间可说是不言自明的。假如还有什么争议，那是在女人中间，绝不是在男人中间。
        当年玛丽莲· 梦露的三围从上面数，好像是三十四、二十二、三十四（英寸）。有位太太看这个小妖精太讨厌，就自己掏钱买了一套内衣给她寄去，尺寸是二十二、三十四、二十二，让她按这个尺寸练练，煞煞男人的火。据我所知，梦露小姐没有接受她的意见。
        这是说到身材，还没说到化妆不化妆、打扮不打扮。这类题目只有在女人杂志上才是中心议题，我所认识的男人在这方面都有一颗平常心，也就是说，见到好看的女人就多看一眼，见到不好看的就少看一眼，仅此而已。多看一眼和少看一眼都没什么严重性。所以我认为，在我们这里，这问题在女人中比在男人中敏感。
        大贤罗素曾说：人人理应生来平等。但很可惜，事实不是这样。有人生来漂亮,有人生来就不漂亮.与男人相比，女人更觉得自己是这种不平等的牺牲品。至于如何来消除这种不平等，就有各种解决的办法。给梦露小姐寄内衣的那位太太就提出了一种解法，假设那套内衣是她本人穿的，这就意味着请梦露向她看齐；假如这个办法被普遍地采用，那么男人会成为真正的牺牲品。
        在国外可以看到另一种解决不平等的方法,那里年轻漂亮的小姐们不怎么化妆，倒是中老年妇女总是要化点妆。这样从总体上看，大家都相当漂亮。另外，年轻、健康，这本身就是最美丽的，用不着用化妆品来掩盖它。我觉得这样做有相当的合理性。国内的情况则相反，越是年轻漂亮的小姐越要化妆，上点岁数的就破罐破摔，蓬头垢面—我以为这是不好的。
        假如有一位妇女修饰得恰到好处地出现在我面前，我是很高兴的。这说明她在乎我对她的看法，对我来说是一种尊重。但若修饰不得法，就是一种灾难。几年前，我到北方一座城市出差，看到当地的小姐们都化妆，涂很重的粉，但那种粉颜色有点发蓝，走在阳光灿烂的大街上尚称好看，走到了暗处就让人想起了戏台上的窦尔敦。
        另外，当地的小姐都穿一种针织超短裙，大概此种裙子很是新潮，但有一处弊病，就是会朝上收缩，走在街上裙子就会呈现一种倒马鞍形。于是常能看到有些很可爱的妇女走在当街叉开腿站下来，用手抓住裙子的下摆往下拉—那情景实在可怕。所以我建议女同志们在选购时装和化妆品时要多用些心，否则穿得随便一点，不化妆会更好一点。
        对于妇女在外貌方面的焦虑情绪，男人的平常心是一副解毒剂。另外，还该提到女权主义者的看法，她们说:我们干吗要给男人打扮？这话有些道理，也有点过激。假如修饰自己意味着尊重对方，还是打扮一下好。""",

        """如果按照正常的标准来看，我大概很快就要丧失撰写饮食文章的资格，因为我素食的倾向愈来愈强，搞不好那天就要开始守斋戒了。
        然而，我又很能体会蔡澜先生未能食素的心境。不知道其他人有没有这种经历，如果一桌人坐下来点菜，其中一个事先声明吃斋的话，邻座可能会觉得自己被人冒犯了。为什么？因为素食者总给人一种异样的道德优越感，总是使人以为他的伦理标准比较高，自律能力比较强。而大伙吃饭本来是件很愉快甚至很纵欲的一件事，突然旁边多了一个禁欲主义者，岂能不叫人扫兴？这就有点像一堆黑社会的小流氓正在肆无忌惮地粗口横飞，大佬身边的“阿嫂”忽然冷冷地道一句：“我本人唔系咁中意讲粗口”。
        其实我是有亲身体会的。很多年前，和一个后来出了家的同学在大排档吃饭叙旧，正当弟兄们兴高采烈地要叫几瓶冰冻啤酒时，他却平静和缓地说：“其实我已经吃斋了”。我们很愕然，一起转头看着他那仿佛散发着天使光采的慈善面容，他又接着说：“没关系！不用理我，你们尽管叫尽管吃，我要碗粥就行了”。那一刻，我感到自己就像一个野蛮的食人族遇上了从文明社会过来传教的牧师，羞愧难当。我是不是该把他也煮来吃了呢？"""
    ]

    for text in texts:
        assert len(special_chars(text)) > 0
        text = process_text_cn(text)
        assert len(special_chars(text)) == 0
        parts = list(split_text_by_length(text, max_length=200,
                                          min_length=150))
        for part in parts[:-1]:
            assert 150 <= len(part) <= 200
            assert part.endswith(tuple("”’】）。！？；～…，"))

        assert len(parts[-1]) <= 200
