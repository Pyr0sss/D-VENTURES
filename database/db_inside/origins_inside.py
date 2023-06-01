from database.models.origin_model import Origin

def new_origin(name, desc):
    Origin.create(origin_name = name, origin_description = desc)

def origins():
    origins_list = ["Прислужник 📿", "Шарлатан 🃏", "Преступник 🦹", "Артист 🎤", "Народный герой 👮‍",
           "Гильдейский ремесленник 💰", "Отшельник 🌅", "Благородный 👑", "Чуземец 🌎",
           "Мудрец 🧔‍", "Моряк 🚢", "Солдат 🪖", "Беспризорник 👦"]
    desc_list = [
        "Вы провели свою жизнь, служа в храме, посвящённому какому-то конкретному богу или же пантеону богов. Вы — посредник между царством небесным и миром живых. Вы совершали священные ритуалы и приносили жертвоприношения для того чтобы молящиеся могли предстать пред ликом богов. Вы не обязательно жрец — совершение священных обрядов не то же самое, что направление божественной силы. Вы были младшим служкой в храме, с детства помогающим священникам? Или вы верховный жрец, получивший видение, как можно послужить своему богу? Возможно, вы — лидер небольшого культа, не имеющего своего храма, или даже представитель оккультных сил, служивший чудовищному повелителю, но отрёкшийся от него.",
        "Вы хорошо знаете людей. Вы понимаете, что ими движет, и можете распознать их самые сокровенные желания спустя всего пару минут после начала разговора. Несколько наводящих вопросов, и вот вы уже читаете их словно книжки, написанные для детей. Это полезный талант, и вы вполне готовы использовать его себе на благо. Вы знаете, что люди хотят, и вы даёте им это, или же обещаете дать. Чувство здравого смысла должно заставлять людей держаться подальше от тех вещей, которые слишком хорошо звучат, чтобы быть правдой. Но здравый смысл куда-то улетучивается, когда вы неподалёку. Бутылочка с розовой жидкостью всенепременно вылечит эту неблаговидную сыпь, а эта чудодейственная мазь (не более чем горсть жира, смешанного с серебряной пылью) без сомнения вернёт молодость и энергичность. Все эти чудеса, конечно, звучат неправдоподобно, но вы знаете, как преподнести их так, чтобы они казались крайне выгодным делом.",
        "Вы опытный преступник с большим послужным списком. Вы провели много времени, вращаясь в преступных кругах, и до сих пор имеете связи с подпольным миром. В отличие от обычных людей вы близко познакомились с убийствами, воровством и жестокостью, что пропитывают низшие слои общества. Вы научились выживать, пренебрегая правилами и ограничениями, которым подчиняются другие.",
        "Вам нравится выступать на публике. Вы знаете, как их развлечь, очаровать и даже воодушевить. Ваша поэзия может трогать сердца слушателей, пробуждать в них горе или радость, смех или гнев. Ваша музыка ободряет их или заставляет скорбеть. Ваши танцы захватывают, а шутки всегда смешны. Чем бы вы ни занимались, ваша жизнь тесно связана с искусством.",
        "У вас было низкое социальное положение, но судьбой было уготовано большее. Жители вашей родной деревни уже считают вас своим героем, но вам предначертано сражаться с тиранами и чудовищами, угрожающими другим.",
        "Вы — член гильдии ремесленников, знаток в какой-то области, связанный с другими мастеровыми. Вы крепко стоите на ногах в этом торгашеском мире, отделённые своим талантом и богатством от оков феодального строя. Когда-то вы учились у мастера, под опекой гильдии, и вот вы сами стали таким умельцем.",
        "Вы значительную часть своей жизни прожили в уединении — либо в закрытой общине, такой как монастырь, либо вообще в одиночестве. Вдали от шумного общества вы нашли тишину, спокойствие, а возможно, и ответы на важные вопросы.",
        "Вы знаете, что такое богатство, власть и привилегии. У вас благородный титул, а ваша семья владеет землями, собирает налоги, и обладает серьёзным политическим влиянием. Вы можете быть изнеженным аристократом, незнакомым с работой и неудобствами, бывшим торговцем, только-только получившим титул, или лишённым наследства негодяем с гипертрофированным чувством собственного права. Или же вы можете быть честным, трудолюбивым землевладельцем, искренне заботящимся о тех, кто живёт и трудится на его земле, ощущая за них ответственность. Придумайте вместе с Мастером надлежащий титул и определите, какую власть этот титул даёт. Благородный титул не существует сам по себе — он связан со всей вашей семьёй, и каким бы титулом вы ни обладали, вы передадите его своим детям. Вам нужно не только определить титул, но также описать вместе с Мастером вашу семью и её влияние на вас.",
        "Вы выросли в глуши, вдали от цивилизации и её благ. Вы видели миграцию стад, чей размер был больше леса, выживали при температуре, которую горожанам и не представить, и наслаждались таким уединением, что на многие мили вокруг вы были единственным мыслящим существом. Дикая природа в вашей крови, будь вы кочевником, исследователем, затворником, охотником-собирателем или даже мародёром. Даже в неизвестном месте вы найдёте что-то, что вам понятно.",
        "Вы провели много лет, постигая тайны мультивселенной. Вы читали рукописи, изучали свитки, и общались с величайшими экспертами в интересующих вас темах. Всё это сделало вас знатоком в своей области.",
        "Вы много лет плавали на морском судне. Вы видели могучие шторма, глубоководных чудовищ и тех, кто хотел отправить вас на дно. Первая любовь осталась далеко за горизонтом, и настало время попробовать что-то новое. Решите вместе с Мастером, на каком корабле вы до этого плавали. Это было торговое, пассажирское, исследовательское или пиратское судно? Насколько оно прославилось (в хорошем или дурном смысле)? Много ли вы путешествовали? Оно всё еще на плаву, потоплено или утеряно?",
        "Сколько вы помните, в вашей жизни всегда была война. С молодости вы проходили тренировки, учились использовать оружие и доспехи, изучали технику выживания, включая то, как оставаться живым на поле боя. Вы могли быть частью армии страны или отряда наёмников, а может, были местным ополченцем во время войны. Выбрав эту предысторию, определите вместе с Мастером, в какой военной организации вы состояли, до какого звания вы дослужились, и что вам за это время довелось пережить. Что это было, регулярная армия, городская стража или деревенское ополчение? Это могла быть частная армия наёмников дворянина или самостоятельный бродячий отряд наёмников.",
        "Вы выросли на улице в бедности и одиночестве, лишённые родителей. Никто не присматривал и не заботился о вас, и вам пришлось научиться делать это самому. Вам приходилось постоянно бороться за еду и следить за другими неприкаянными душами, способными обокрасть вас. Вы спали на чердаках и в переулках, мокли под дождём и боролись с болезнями, не получая медицинской помощи или приюта. Вы выжили, невзирая на все трудности, и сделали это благодаря своей сноровке, силе или скорости. Вы начинаете приключение с суммой денег, достаточной, чтоб скромно, но уверенно прожить десять дней. Как вы получили эти деньги? Что позволило вам перейти к нормальной жизни, преодолев нищету?"]
    for i in range(len(origins_list)):
        new_origin(origins_list[i], desc_list[i])