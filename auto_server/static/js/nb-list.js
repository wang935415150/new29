/**
 * Created by Administrator on 2017/10/11.
 */


(function (jq) {


    
    var requestUrl = "";
    var GLOBAL_CHOICES_DICT = {
        // 'status_choices': [[0,'xxx'],]
        // 'xxxx_choices': [[0,'xxx'],]
    };

    function  getChoiceNameById(choice_name,id) {
        var val;

        var status_choices_list = GLOBAL_CHOICES_DICT[choice_name];
        $.each(status_choices_list,function (kkkk,vvvv) {
              if(id == vvvv[0]){
                  val = vvvv[1];
              }
        });
        return val;
    }


    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    /*
    像后台获取数据
     */
    function init(pageNum) {
        $('#loading').removeClass('hide');

        var condition = getSearchCondition();
        console.log(condition);
        $.ajax({
            url:requestUrl,
            type: 'GET',
            data: {'pageNum':pageNum,'condition':condition},
            dataType: 'JSON',
            success:function (response) {


                /* 处理choice */
                GLOBAL_CHOICES_DICT = response.global_choices_dict;

                 /* 处理搜索条件 */
                initSearchCondition(response.search_config);


                /* 处理表头 */
                initTableHead(response.table_config);

                /* 处理表内容 */
                initTableBody(response.data_list,response.table_config);

                /* 处理表分页 */
                initPageHtml(response.page_html);


                $('#loading').addClass('hide');
            },
            error:function () {
                $('#loading').addClass('hide');
            }
        })

    }

    /*
    绑定搜索条件事件
     */
    function bindSearchConditionEvent() {
        /* 改变下拉框内容时*/
        $('#searchCondition').on('click','li',function () {
            // $(this) = li标签

            // 找到文本修改
            $(this).parent().prev().prev().text($(this).text());

            // 找input标签，修改，重建
            $(this).parent().parent().next().remove();

            var name = $(this).find('a').attr('name');
            var type = $(this).find('a').attr('type');
            if(type=='select'){
                var choice_name = $(this).find('a').attr('choice_name');

                // 作业：生成下拉框，
                var tag = document.createElement('select');
                tag.className = "form-control no-radius";
                tag.setAttribute('name',name);
                $.each(GLOBAL_CHOICES_DICT[choice_name],function(i,item){
                    var op = document.createElement('option');
                    op.innerHTML = item[1];
                    op.setAttribute('value',item[0]);
                    $(tag).append(op);
                })
            }else{
                // <input class="form-control no-radius" placeholder="逗号分割多条件" name="hostnmae">
                var tag = document.createElement('input');
                tag.setAttribute('type','text');
                // $(tag).addClass('form-control no-radius')
                tag.className = "form-control no-radius";
                tag.setAttribute('placeholder','请输入条件');
                tag.setAttribute('name',name);
            }

            $(this).parent().parent().after(tag);

        });


        /* 添加搜索条件 */
        $('#searchCondition .add-condition').click(function () {

            var $condition = $(this).parent().parent().clone();
            $condition.find('.add-condition').removeClass('add-condition').addClass('del-condition').find('i').attr('class','fa fa-minus-square');

            // $(this).parent().parent().parent().append($condition);
            // $('#searchCondition').append($condition);
            $condition.appendTo($('#searchCondition'));
        });

        /* 删除搜索条件 */
        $('#searchCondition').on('click','.del-condition',function () {
            $(this).parent().parent().remove();
        });

        /* 点击搜索按钮 */
        $('#doSearch').click(function () {
            init(1);
        })
        
    }
    
    function initSearchCondition(searchConfig) {
        if(!$('#searchCondition').attr('init')){
            // 找到页面上的搜索条件标签
            // 根据searchConfig生成li
            var $ul = $('#searchCondition :first').find('ul');
            $ul.empty();

            initDefaultSearchCondition(searchConfig[0]);

            $.each(searchConfig,function (i,item) {
                var li = document.createElement('li');
                var a =  document.createElement('a');
                a.innerHTML = item.title;
                a.setAttribute('name',item.name);
                a.setAttribute('type',item.type);
                if(item.type == 'select'){
                    a.setAttribute('choice_name',item.choice_name);
                }

                $(li).append(a);
                $ul.append(li);

            });

            $('#searchCondition').attr('init','true');

        }




    }
    
    function initDefaultSearchCondition(item) {
        // item={'name': 'hostname','title':'主机名','type':'input'},
        if(item.type == 'input'){
            var tag = document.createElement('input');
            tag.setAttribute('type','text');
            // $(tag).addClass('form-control no-radius')
            tag.className = "form-control no-radius";
            tag.setAttribute('placeholder','请输入条件');
            tag.setAttribute('name',item.name);

        }else{
            var tag = document.createElement('select');
            tag.className = "form-control no-radius";
            tag.setAttribute('name',item.name);
            $.each(GLOBAL_CHOICES_DICT[item.choice_name],function(i,row){
                var op = document.createElement('option');
                op.innerHTML = row[1];
                op.setAttribute('value',row[0]);
                $(tag).append(op);
            })
        }

        $('#searchCondition').find('.input-group').append(tag);
        $('#searchCondition').find('.input-group label').text(item.title);
    }

    function getSearchCondition() {
        // 找所有input,select
        // 作业：result数据格式为：
        /*
             {
                server_status_id: [1,2],
                hostname: ['c1.com','c2.com']
            }
         */
        var result = {};
        $('#searchCondition').find('input[type="text"],select').each(function(){
            var name = $(this).attr('name');
            var val = $(this).val();
            if (result[name]){
                result[name].push(val)
            }else {
                result[name] = [val,]
            }
        });
        return result;
    }


    function initPageHtml(page_html) {
        $('#pagination').empty().append(page_html);
    }
    
    function initTableHead(table_config) {
        /*
         table_config = [
                {
                    'q': 'hostname',
                    'title': '主机名',
                },
                {
                    'q': 'sn',
                    'title': '序列号',
                },
                {
                    'q': 'os_platform',
                    'title': '系统',
                },
            ]
         */
        $('#tHead tr').empty();
            $.each(table_config,function (k,conf) {
                if(conf.display){
                    var th = document.createElement('th');
                    th.innerHTML = conf.title;
                    $('#tHead tr').append(th);
                }
            });
    }

    function initTableBody(data_list,table_config) {
        /*
        [
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
            {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},
        ]

        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td></td>
        </tr>

         */
        $('#tBody').empty();

        $.each(data_list,function (k,row_dict) {
            // 循环数据库中获取到的每行数据
            // row_dict = {'hostname':'xx', 'sn':'xx', 'os_platform':'xxx'},

            var tr = document.createElement('tr');

            $.each(table_config,function (kk,vv) {
                if(vv.display){
                    var td = document.createElement('td');


                    /* 处理Td内容 */
                    var format_dict = {};
                    $.each(vv.text.kwargs,function (kkk,vvv) {
                        if(vvv.substring(0,2) == "@@"){
                            var name = vvv.substring(2,vvv.length); // status_choices
                            var val = getChoiceNameById(name,row_dict[vv.q]);
                            format_dict[kkk] = val;
                        }
                        else if(vvv[0] == "@"){
                            var name = vvv.substring(1,vvv.length);
                            format_dict[kkk] = row_dict[name];
                        }else{
                            format_dict[kkk] = vvv;
                        }
                    });

                    td.innerHTML = vv.text.tpl.format(format_dict);

                    /* 处理Td属性 */
                    $.each(vv.attr,function(attrName,attrVal){
                        if(attrVal[0] == "@"){
                            attrVal = row_dict[attrVal.substring(1,attrVal.length)]
                        }
                       td.setAttribute(attrName,attrVal);
                    });


                    $(tr).append(td);
                }
            });

            $('#tBody').append(tr);
        })

    }

    jq.extend({
        "nBList":function (url) {
            requestUrl = url;
            init(1);
            bindSearchConditionEvent();
        },
        "changePage":function (pageNum) {
            init(pageNum);
        }
    });

})(jQuery);




