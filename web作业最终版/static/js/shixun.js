// $(function() {
//     $("#captcha-btn").click(function(event) {
//         // 阻止默认的事件
//         event.preventDefault();
//
//         var email = $("input[name='email']").val();
//         var $this =$(this); // 将当前的按钮元素存储到变量中
//
//         $.ajax({
//             url: "/auth/captcha/email?email=" + email,
//             method: "GET"
//         }).done(function(result) { // 使用 done 替代 success
//             var code = result['code'];
//             if (code == 200) {
//                 var countdown = 60;
//                 $this.off("click"); // 使用$this 来移除点击事件
//                 var timer = setInterval(function() {
//                     $this.text(countdown);
//                     countdown -= 1;
//                     if (countdown <= 0) {
//                         clearInterval(timer);
//                         $this.text("获取验证码");
//                         $this.on("click", function(event) { // 重新绑定点击事件
//                             // 这里可以再次绑定点击事件的处理逻辑
//                         });
//                     }
//                 }, 1000); // 设置定时器间隔为1000毫秒
//             }
//         }).fail(function(error) { // 使用 fail 替代 error
//             console.log(error);
//         });
//     });
// });
