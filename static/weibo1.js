var apiWeiboAll = function(id, callback) {
    var path = `/ajax/weibo/all?author_id=${id}`
    ajax('GET', path, '', callback)
}


var weiboTemplate = function(weibo) {
    var w = `
        <div class="weibo-cell" id=weibo${weibo.id}>
            <span class="weibo-content">${weibo.content} </span>
            <!--<button data-id=${weibo.id} class="weibo-delete">删除</button>-->
            <!--<button data-id=${weibo.id} class="weibo-edit">编辑</button>-->
            <br>
            <input class='input-comment'>
            <button data-id=${weibo.id} class='button-comment'>add</button>
            <br>
            <br>
        </div>
    `
    return w
}

var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var loadWeibos = function() {
    var user = e('#id-input-visit')
    var id = user.value
    apiWeiboAll(id, function(r) {
        console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}

var __main = function() {
    loadWeibos()
}

__main()
