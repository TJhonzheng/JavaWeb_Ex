<template>
  <div class="userInfo">
    <el-upload
      class="avatar-uploader"
      action="no"
      :show-file-list="false"
      :on-success="handleAvatarSuccess"
      :before-upload="beforeAvatarUpload">
      <img v-if="imageUrl" :src="imageUrl" class="avatar">
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
    </el-upload>
    <el-form ref="form" :model="form" :rules="rules" label-width="70px">
      <el-form-item label="账号" prop="username">
        <el-tag>{{this.username}}</el-tag>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-tag>{{this.email}}</el-tag>
      </el-form-item>
      <el-form-item label="性别" prop="sex">
        <el-switch v-model="form.sex" active-text="男" inactive-text="女" inactive-color="#f56c6c" :disabled="!judge"></el-switch>
      </el-form-item>
      <el-form-item label="昵称" prop="nickName">
        <el-input v-model="form.nickName" autocomplete="off" :disabled="!judge"></el-input>
      </el-form-item>
      <el-form-item label="生日" prop="birthday">
        <el-date-picker type="date" placeholder="选择日期" :picker-options="pickerOptions" v-model="form.birthday" style="width:100%;" :disabled="!judge"></el-date-picker>
      </el-form-item>
      <el-form-item label="签名" prop="selfInfo">
        <el-input type="textarea" v-model="form.selfInfo"  placeholder="最长不能超过150个字符" autocomplete="off" :disabled="!judge"></el-input>
      </el-form-item>
    </el-form>
    <div class="buttonGroup">
      <el-button type="primary" @click="judge=true" :disabled="judge">编辑</el-button>
      <el-button type="primary" @click="submitForm('form')" :disabled="!judge">保存</el-button>
    </div>

  </div>
</template>

<script>
  export default {
    name: "userinfo",
    mounted(){
      this.userId = sessionStorage.getItem('userId')
      this.username = sessionStorage.getItem('username')
      this.email = sessionStorage.getItem('email')
      this.$api.user.getMessage({
        id:this.userId
      }).then((res)=>{
        if(res.data.status===0){
          console.log(res)
          let info = res.data
          this.form.nickName = info['Unickname'];
          let sex = info['USex']
          this.form.sex = sex === 'M';
          this.imageUrl = info['img']
          if(info['UBirthday'] !== 0)
            this.form.birthday = new Date(Date.parse(info['UBirthday']))
          else this.form.birthday = new Date()
          this.form.selfInfo = info['UStatement']
        }
        else{
          console.log(res.data.message)
        }
      })
    },
    data(){
      var checkNickName = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('用户昵称不能为空'));
        }
        setTimeout(()=>{
          callback();
        },1000);
      };
      return{
        judge:false,
        userId:null,
        username:'',
        email:'',
        imageUrl:'',
        form:{
          nickName:'',
          sex:true,
          birthday:'',
          selfInfo:'',
          sexString:''
        },
        rules:{
          nickName: [
            { validator: checkNickName, trigger: 'blur' }
          ],
        },
        pickerOptions: {
          disabledDate(time) {
            return time.getTime() > Date.now();
          },
        }
      }
    },
    methods:{
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isPNG= file.type === 'image/png';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG && !isPNG) {
          this.$message.error('上传头像图片只能是 JPG 格式或 PNG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        let fd = new FormData()
        fd.append('img', file)
        fd.append('userId', this.userId)
        let config = {
          headers:{'Content-Type':'multipart/form-data'} //这里是重点，需要和后台沟通好请求头，Content-Type不一定是这个值
        };
        this.$api.user.upLoadImage(fd, config).then((res)=>{
          this.imageUrl = res.data.img
          sessionStorage.setItem('imgurl', res.data.img)
          this.$emit('childsay1', res.data.img)
        })
        return isJPG && isLt2M;
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.form.sex)
              this.sexString = 'M'
            else this.sexString = 'F'
            console.log(this.form.nickName)
            this.$api.user.alterMessage({
              id:this.userId,
              nickname:this.form.nickName,
              sex:this.sexString,
              statement:this.form.selfInfo,
              birthday:this.form.birthday
            }).then((res)=>{
                if(res.data.status==0){
                  sessionStorage.setItem('nickName', this.form.nickName)
                  this.$emit('childsay', this.form.nickName)
                  this.$message.success('用户信息修改成功！')
                  this.judge = false
                }else {
                  this.$message.error(res.data.message);
                }
              }
            )
          } else {
            this.$message.error('请完善信息！');
          }

        })

      },
    }
  }
</script>

<style lang="scss">
  .userInfo{
    .avatar-uploader .el-upload {
      border: 1.5px dashed #d9d9d9;
      border-radius: 50%;
      cursor: pointer;
      position: absolute;
      overflow: hidden;
      right:70px;
      top:80px;
    }
    .avatar-uploader .el-upload:hover {
      border-color: #409EFF;
    }
    .avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 160px;
      height: 160px;
      line-height: 160px;
      text-align: center;
    }
    .avatar {
      width: 160px;
      height: 160px;
      display: block;
    }
    .buttonGroup{
      display:flex;
      justify-content: center;
      align-items: center;
      flex-direction: row;
      .el-button{
        width:30%;
        border-radius: 30px;
      }
    }
    .el-tag{
      font-size:15px;
    }
  }
</style>
