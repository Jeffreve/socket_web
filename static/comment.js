var apiCommentAll = function(visitId, callback) {
    var path = `/ajax/comment/all?author_id=${visitId}`
    ajax('GET', path, '', callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/ajax/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(id, callback) {
    var path = `/ajax/comment/delete?id=${id}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/ajax/comment/update'
    ajax('POST', path, form, callback)
}

var commentTemplate = function(userId, comment) {
    if (Number(userId) === comment.user_id){
        var editButton = `<button data-id=${comment.id} class="comment-edit">编辑</button>`
    }
    else{
        var editButton =''
    }

    if ((Number(userId) === comment.user_id) || (Number(userId) === comment.weibo_user_id)){
        var deleteButton = `<button data-id=${comment.id} class="comment-delete">删除</button>`
    }
    else{
        var deleteButton =''
    }

    var w = `
        <div class="comment-cell" id=comment${comment.id}>
            <span class="comment-content">${comment.content} from </span>
            <span>${comment.user}</span>
            ${ editButton }
            ${ deleteButton }
            <br>
            <br>
        </div>
    `
    return w
}

var commentUpdateTemplate = function(commentId) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input">
            <button data-id=${commentId} class="comment-update">更新</button>
            <br>
            <br>
        </div>
    `
    return t
}


var insertComment = function(userId, comment) {
    var commentCell = commentTemplate(userId, comment)
    var q = `#weibo${comment.weibo_id}`
    var weiboCell = e(q)
    weiboCell.insertAdjacentHTML('beforeend', commentCell)
}

var insertCommentUpdate = function(edit_button) {
    var commentId = edit_button.dataset.id
    var editCell = commentUpdateTemplate(commentId)
    edit_button.parentElement.insertAdjacentHTML('beforeend', editCell)
}

var loadComments = function() {
    var user = e('#id-input-user')
    var userId = user.value
    var visit = e('#id-input-visit')
    var visitId = visit.value
    apiCommentAll(visitId, function(r) {
        console.log('load all1', r)
        // 解析为 数组
        var comments = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < comments.length; i++) {
            var comment = comments[i]
            insertComment(userId, comment)
        }
    })
}

var bindEventCommentAdd = function() {
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('button-comment')) {
            log('点到了 更新按钮，id 是', self.dataset.id )
            var weiboCell = self.closest('.weibo-cell')
            var input = weiboCell.querySelector('.input-comment')
            var weiboId = self.dataset.id
            var visit = e('#id-input-visit')
            var user = e('#id-input-user')
            var userId = user.value
            var visitId = visit.value
            var form = {
                weibo_user_id: visitId,
                weibo_id: weiboId,
                content: input.value,
            }
            log('form', form)
            apiCommentAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            log('data', r)
            var comment = JSON.parse(r)
            insertComment(userId, comment)
        })
        } else {
            log('点击的不是删除按钮******')
        }
    })
}

var bindEventCommentDelete = function() {
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('comment-delete')) {
            log('点到了 删除按钮，id 是', self.dataset.id )
            var commentId = self.dataset.id
            apiCommentDelete(commentId, function(r) {
                self.parentElement.remove()
            })
        } else {
            log('点击的不是删除按钮******')
        }
    })
}

var bindEventCommentEdit = function(){
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('comment-edit')) {
            log('点到了 comment编辑按钮，id 是', self.dataset.id )
            // 插入编辑输入框
            insertCommentUpdate(self)
        } else {
            log('点击的不是编辑按钮******')
        }
    })
}

var bindEventCommentUpdate = function(){
    var weiboList = e('.weibo-list')
    weiboList.addEventListener('click', function(event){
        var self = event.target
        if (self.classList.contains('comment-update')) {
            log('点到了 更新按钮，id 是', self.dataset.id )
            var commentCell = self.closest('.comment-cell')
            var input = commentCell.querySelector('.comment-update-input')
            var commentId = self.dataset.id
            var form = {
                id: commentId,
                content: input.value,
            }
            apiCommentUpdate(form, function(r){
                log('收到更新数据', r)
                var updateForm = commentCell.querySelector('.comment-update-form')
                updateForm.remove()

                var comment = JSON.parse(r)
                var commentcontent = commentCell.querySelector('.comment-content')
                commentcontent.innerText = comment.content
            })
        } else {
            log('点击的不是更新按钮******')
        }
    })
}

var bindEvents = function() {
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadComments()
}

__main()
