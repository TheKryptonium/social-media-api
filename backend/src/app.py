from fastapi  import FastAPI, HTTPException, File, UploadFile, Form, Depends
from typing import List
from .schemas import PostCreate, PostResponse
from .db import Post, create_db_and_tables, create_async_engine, get_async_session
from .images import imagekit
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
import shutil
import os
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post('/upload')
async def upload_post(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
            
            upload_result = imagekit.files.upload(
                file=open(temp_file_path, "rb"),
                file_name = file.filename,
                use_unique_file_name= True,
                tags=["backend-upload"]    
            )
    
        if upload_result.url:    
            post = Post(
                caption = caption,
                url=upload_result.url ,
                file_type = "video" if file.content_type.startswith("video/") else "image",
                file_name = upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


@app.get('/feed')
async def get_feed(
    session: AsyncSession= Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    
    post_data=[]
    for post in posts:
        post_data.append(
            {
                "id": str(post.id), 
                "caption": post.caption,
                "url": post.url,
                "file_type":post.file_type,
                "file_name":post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
        
    return post_data



@app.delete('/posts/{post_id}')
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)
        
        result = await session.execute(select(Post).where(Post.id== post_uuid))
        post = result.scalars().first()
        
        await session.delete(post)
        await session.commit()
        
        return {"Success": True, "message": "Post deleted succesfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


