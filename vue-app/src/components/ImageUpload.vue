   <template>
     <div>
       <input type="file" @change="previewImage" accept="image/*">
       <button @click="uploadImage">アップロード</button>
       <div v-if="image">
         <img :src="image" alt="Preview">
       </div>
     </div>
   </template>

   <script>
   import axios from 'axios';

   export default {
     data() {
       return {
         image: null,
         imageFile: null,
       };
     },
     methods: {
       previewImage(event) {
         this.imageFile = event.target.files[0];
         this.image = URL.createObjectURL(this.imageFile);
       },
       async uploadImage() {
         if (!this.imageFile) {
           alert('ファイルが選択されていません。');
           return;
         }
         const formData = new FormData();
         formData.append('file', this.imageFile);
         try {
           await axios.post('http://localhost:8000/upload/', formData, {
             headers: {
               'Content-Type': 'multipart/form-data'
             }
           });
           alert('アップロード成功！');
         } catch (error) {
           console.error('アップロードエラー', error);
           alert('アップロード失敗！');
         }
       }
     }
   };
   </script>