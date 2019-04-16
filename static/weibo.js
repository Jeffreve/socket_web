var apiWeiboAll = function(id, callback) {
    var path = `/ajax/weibo/all?author_id=${id}`
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(id, form, callback) {
    var path = `/ajax/weibo/add?author_id=${id}`
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(id, callback) {
    var path = `/ajax/weibo/delete?id=${id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/ajax/weibo/update'
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo) {
    var w = `
        <div class="weibo-cell" id=weibo${weibo.id}>
            <span class="weibo-content">${weibo.content} </span>
            <button data-id=${weibo.id} class="weibo-delete">删除</button>
            <button data-id=${weibo.id} class="weibo-edit">编辑</button>
            <br>
            <input class='input-comment'>
            <button data-id=${weibo.id} class='button-comment'>add</button>
            <br>
            <br>
        </div>
    `
    return w
}

var weiboUpdateTemplate = function(weiboId) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input">
            <button data-id=${weiboId} class="weibo-update">更新</button>
            <br>
            <br>
        </div>
    `
    return t
}


var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertWeiboUpdate = function(edit_button) {
    var weiboId = edit_button.dataset.id
    var editCell = weiboUpdateTemplate(weiboId)
    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}

var loadWeibos = function() {
    var visit = e('#id-input-visit')
    var id = visit.value
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

var bindEventWeiboAdd = function() {
    var user = e('#id-input-visit')
    var id = user.value
    var b = e('#id-button-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(id, form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('weibo-delete')) {
            log('点到了 删除按钮，id 是', self.dataset.id )
            var weiboId = self.dataset.id
            apiWeiboDelete(weiboId, function(r) {
                self.parentElement.remove()
            })
        } else {
            log('点击的不是删除按钮******')
        }
    })
}

var bindEventWeiboEdit = function(){
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('weibo-edit')) {
            log('点到了 weibo编辑按钮，id 是', self.dataset.id )
            // 插入编辑输入框
            insertWeiboUpdate(self)
        } else {
            log('点击的不是编辑按钮******')
        }
    })
}


var bindEventWeiboUpdate = function(){
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('weibo-update')) {
            log('点到了 更新按钮，id 是', self.dataset.id )
            var weiboCell = self.closest('.weibo-cell')
            var input = weiboCell.querySelector('.weibo-update-input')
            var weiboId = self.dataset.id
            var form = {
                id: weiboId,
                content: input.value,
            }

            apiWeiboUpdate(form, function(r){
                log('收到更新数据', r)

                var updateForm = weiboCell.querySelector('.weibo-update-form')
                updateForm.remove()

                var weibo = JSON.parse(r)
                var weibocontent = weiboCell.querySelector('.weibo-content')
                weibocontent.innerText = weibo.content
            })
        } else {
            log('点击的不是更新按钮******')
        }
    })
}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
